# Multi-cloud adaptation

Do not translate every OCI resource line-by-line. Deploy the same application
artifact behind the provider's implementation of the capability contract.

| Capability | OCI | AWS | Azure | GCP |
| --- | --- | --- | --- | --- |
| Compute | Functions/Container Instances | Lambda/ECS | Functions/Container Apps | Cloud Run/Functions |
| API | API Gateway | API Gateway | API Management | API Gateway |
| Database | NoSQL/Autonomous | DynamoDB/Aurora | Cosmos DB/PostgreSQL | Firestore/Cloud SQL |
| Storage | Object Storage | S3 | Blob Storage | Cloud Storage |
| Events | Queue | SQS/EventBridge | Service Bus/Event Grid | Pub/Sub |
| Identity | IAM | IAM/Cognito | Entra ID/Managed Identity | Cloud IAM/Identity Platform |
| Observability | Logging/Monitoring | CloudWatch/X-Ray | Monitor/App Insights | Cloud Operations |

For each provider:

1. implement infrastructure as a provider-specific Terraform module;
2. map outputs to common runtime environment variables;
3. implement only adapters that require provider SDK behavior;
4. execute the same API contract and core tests;
5. add provider integration tests in an isolated account/project/subscription.
