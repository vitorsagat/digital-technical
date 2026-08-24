# OCI deployment from zero

## Prerequisites

- OCI tenancy subscribed to the target region;
- compartment for the environment;
- OCI CLI session or workload identity;
- Terraform 1.5+;
- OCI provider 7.x or 8.x;
- quotas for one VCN, Queue, Log Group, NoSQL table, Functions Application,
  API Gateway, bucket, OCIR repository, and notification topic.

## Least-privilege preparation

Create an environment-specific group or dynamic group. Grant only management of
the resources represented by the module in that compartment. Production policy
must be reviewed by the organization's IAM team. Use Vault for secrets and
Resource Principal for workloads; do not use long-lived user keys in containers.

## Deploy infrastructure

```bash
cd infrastructure/terraform/stacks/oci
cp ../../environments/test/terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -check -recursive
terraform validate
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
```

Store state in an encrypted remote backend with versioning and restricted access.
The example intentionally does not choose an organization-specific backend.

## Deploy the application

1. Build the `Dockerfile` with the organization build service.
2. Scan and sign the image.
3. Push it to the private OCIR repository output by Terraform.
4. Add an `oci_functions_function` resource referencing the immutable image digest.
5. Replace or extend the stock health deployment with a Function backend.
6. Inject database, knowledge, AI, and authentication settings from Vault.
7. Enable API Gateway access logs and application logs in the created Log Group.

The current module deliberately stops before image publication because registry
authentication, signing keys, and approved IAM policies are tenancy-specific.

## Validate and destroy

```bash
curl "$(terraform output -raw api_health_url)"
terraform plan -detailed-exitcode
terraform destroy
```

Confirm corporate lifecycle tags. The Osaka test compartment applies nightly
shutdown and weekly deletion controls.
