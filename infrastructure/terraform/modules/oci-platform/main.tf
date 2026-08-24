locals {
  prefix = "${var.name_prefix}-${var.environment}"
  tags = merge(
    {
      Project     = "DIGITAL TECHNICAL"
      Environment = var.environment
      ManagedBy   = "terraform"
    },
    var.tags,
  )
}

data "oci_objectstorage_namespace" "current" {
  compartment_id = var.compartment_id
}

resource "oci_core_vcn" "main" {
  compartment_id = var.compartment_id
  cidr_blocks    = [var.vcn_cidr]
  display_name   = "${local.prefix}-vcn"
  dns_label      = "dt${substr(var.environment, 0, 3)}"
  freeform_tags  = local.tags
}

resource "oci_core_internet_gateway" "main" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${local.prefix}-igw"
  enabled        = true
  freeform_tags  = local.tags
}

resource "oci_core_route_table" "public" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${local.prefix}-public-routes"
  freeform_tags  = local.tags

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.main.id
  }
}

resource "oci_core_security_list" "app" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "${local.prefix}-security-list"
  freeform_tags  = local.tags

  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
  }

  ingress_security_rules {
    source   = "0.0.0.0/0"
    protocol = "6"

    tcp_options {
      min = 443
      max = 443
    }
  }
}

resource "oci_core_subnet" "app" {
  compartment_id             = var.compartment_id
  vcn_id                     = oci_core_vcn.main.id
  cidr_block                 = var.subnet_cidr
  display_name               = "${local.prefix}-subnet"
  dns_label                  = "app"
  prohibit_public_ip_on_vnic = false
  route_table_id             = oci_core_route_table.public.id
  security_list_ids          = [oci_core_security_list.app.id]
  freeform_tags              = local.tags
}

resource "oci_objectstorage_bucket" "knowledge" {
  compartment_id = var.compartment_id
  namespace      = data.oci_objectstorage_namespace.current.namespace
  name           = "${local.prefix}-knowledge-${var.bucket_suffix}"
  access_type    = "NoPublicAccess"
  storage_tier   = "Standard"
  versioning     = "Enabled"
  freeform_tags  = local.tags
}

resource "oci_queue_queue" "requests" {
  compartment_id                   = var.compartment_id
  display_name                     = "${local.prefix}-requests"
  retention_in_seconds             = 86400
  visibility_in_seconds            = 30
  dead_letter_queue_delivery_count = 5
  freeform_tags                    = local.tags
}

resource "oci_nosql_table" "requests" {
  compartment_id = var.compartment_id
  name           = "DigitalTechnicalRequests${title(var.environment)}"
  ddl_statement  = "CREATE TABLE DigitalTechnicalRequests${title(var.environment)} (requestId STRING, status STRING, criticality STRING, question STRING, response STRING, updatedAt TIMESTAMP(3), PRIMARY KEY(SHARD(requestId)))"
  freeform_tags  = local.tags

  table_limits {
    capacity_mode      = "PROVISIONED"
    max_read_units     = var.nosql_read_units
    max_write_units    = var.nosql_write_units
    max_storage_in_gbs = 1
  }
}

resource "oci_functions_application" "advisor" {
  compartment_id = var.compartment_id
  display_name   = "${local.prefix}-functions"
  subnet_ids     = [oci_core_subnet.app.id]
  freeform_tags  = local.tags

  config = {
    COMPARTMENT_ID   = var.compartment_id
    QUEUE_ID         = oci_queue_queue.requests.id
    NOSQL_TABLE      = oci_nosql_table.requests.name
    KNOWLEDGE_BUCKET = oci_objectstorage_bucket.knowledge.name
    AI_PROVIDER      = "deterministic"
  }
}

resource "oci_artifacts_container_repository" "advisor" {
  compartment_id = var.compartment_id
  display_name   = "${local.prefix}/advisor"
  is_immutable   = false
  is_public      = false
  freeform_tags  = local.tags
}

resource "oci_apigateway_gateway" "advisor" {
  compartment_id = var.compartment_id
  display_name   = "${local.prefix}-gateway"
  endpoint_type  = "PUBLIC"
  subnet_id      = oci_core_subnet.app.id
  freeform_tags  = local.tags
}

resource "oci_apigateway_deployment" "health" {
  compartment_id = var.compartment_id
  gateway_id     = oci_apigateway_gateway.advisor.id
  display_name   = "${local.prefix}-health-api"
  path_prefix    = "/advisor"
  freeform_tags  = local.tags

  specification {
    routes {
      path    = "/health"
      methods = ["GET"]

      backend {
        type   = "STOCK_RESPONSE_BACKEND"
        status = 200
        body = jsonencode({
          service     = "DIGITAL TECHNICAL"
          status      = "ok"
          region      = var.region
          environment = var.environment
        })
      }
    }
  }
}

resource "oci_ons_notification_topic" "operations" {
  compartment_id = var.compartment_id
  name           = "${local.prefix}-operations"
  description    = "DIGITAL TECHNICAL operational notifications."
  freeform_tags  = local.tags
}

resource "oci_logging_log_group" "advisor" {
  compartment_id = var.compartment_id
  display_name   = "${local.prefix}-logs"
  description    = "DIGITAL TECHNICAL application logs."
  freeform_tags  = local.tags
}
