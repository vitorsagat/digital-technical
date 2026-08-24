from dataclasses import dataclass


@dataclass(frozen=True)
class CloudCapabilities:
    compute: str
    api_gateway: str
    database: str
    object_storage: str
    messaging: str
    observability: str
    identity: str


CLOUD_PROVIDERS = {
    "oci": CloudCapabilities(
        "OCI Functions",
        "API Gateway",
        "NoSQL/Autonomous Database",
        "Object Storage",
        "Queue",
        "Logging/Monitoring",
        "IAM",
    ),
    "aws": CloudCapabilities(
        "Lambda",
        "API Gateway",
        "DynamoDB/Aurora",
        "S3",
        "SQS",
        "CloudWatch",
        "IAM/Cognito",
    ),
    "azure": CloudCapabilities(
        "Azure Functions",
        "API Management",
        "Cosmos DB/PostgreSQL",
        "Blob Storage",
        "Service Bus",
        "Azure Monitor",
        "Entra ID",
    ),
    "gcp": CloudCapabilities(
        "Cloud Run/Functions",
        "API Gateway",
        "Firestore/Cloud SQL",
        "Cloud Storage",
        "Pub/Sub",
        "Cloud Operations",
        "Cloud IAM/Identity Platform",
    ),
}


def get_cloud_capabilities(provider: str) -> CloudCapabilities:
    try:
        return CLOUD_PROVIDERS[provider]
    except KeyError as error:
        raise ValueError(f"Unsupported cloud provider: {provider}") from error
