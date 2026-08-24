# Terraform

The `modules/oci-platform` module owns provider-specific resources. The `stacks/oci`
root configures the provider and calls the module. Environment files contain only
non-secret examples and are never used as state backends.

```bash
cd infrastructure/terraform/stacks/oci
terraform init
terraform plan \
  -var-file=../../environments/dev/terraform.tfvars
terraform apply \
  -var-file=../../environments/dev/terraform.tfvars
```

Copy an example to `terraform.tfvars` and replace placeholders. Do not commit the
result. Configure a remote encrypted backend and state locking before team use.

The business application is not represented in this module. A future AWS, Azure,
or GCP stack should implement the capability contract documented in
`docs/architecture/provider-contract.md`, while reusing the same container and API.
