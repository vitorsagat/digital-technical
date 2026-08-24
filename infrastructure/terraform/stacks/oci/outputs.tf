output "platform" {
  value = {
    api_health_url           = module.platform.api_health_url
    functions_application_id = module.platform.functions_application_id
    container_repository     = module.platform.container_repository
    knowledge_bucket         = module.platform.knowledge_bucket
    nosql_table              = module.platform.nosql_table
    queue_id                 = module.platform.queue_id
    network                  = module.platform.network
  }
}
