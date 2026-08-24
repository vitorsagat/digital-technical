terraform {
  required_version = ">= 1.5.0"

  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 7.0.0, < 9.0.0"
    }
  }
}

provider "oci" {
  region = var.region
}

module "platform" {
  source = "../../modules/oci-platform"

  compartment_id    = var.compartment_id
  region            = var.region
  environment       = var.environment
  bucket_suffix     = var.bucket_suffix
  name_prefix       = var.name_prefix
  vcn_cidr          = var.vcn_cidr
  subnet_cidr       = var.subnet_cidr
  nosql_read_units  = var.nosql_read_units
  nosql_write_units = var.nosql_write_units
  tags              = var.tags
}
