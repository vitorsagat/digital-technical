output "api_health_url" {
  value       = "https://${oci_apigateway_gateway.advisor.hostname}/advisor/health"
  description = "Public health endpoint."
}

output "functions_application_id" {
  value = oci_functions_application.advisor.id
}

output "container_repository" {
  value = oci_artifacts_container_repository.advisor.display_name
}

output "knowledge_bucket" {
  value = oci_objectstorage_bucket.knowledge.name
}

output "nosql_table" {
  value = oci_nosql_table.requests.name
}

output "queue_id" {
  value = oci_queue_queue.requests.id
}

output "network" {
  value = {
    vcn_id    = oci_core_vcn.main.id
    subnet_id = oci_core_subnet.app.id
  }
}
