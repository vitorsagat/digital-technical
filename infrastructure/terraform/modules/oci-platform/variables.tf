variable "compartment_id" {
  type        = string
  description = "OCI compartment OCID."
}

variable "region" {
  type        = string
  description = "OCI region identifier."
}

variable "environment" {
  type        = string
  description = "Deployment environment."

  validation {
    condition     = contains(["dev", "test", "staging", "production"], var.environment)
    error_message = "environment must be dev, test, staging, or production."
  }
}

variable "name_prefix" {
  type        = string
  description = "Resource name prefix."
  default     = "digital-technical"
}

variable "bucket_suffix" {
  type        = string
  description = "Globally unique bucket suffix."
}

variable "vcn_cidr" {
  type        = string
  description = "VCN CIDR."
  default     = "10.42.0.0/16"
}

variable "subnet_cidr" {
  type        = string
  description = "Application subnet CIDR."
  default     = "10.42.10.0/24"
}

variable "nosql_read_units" {
  type        = number
  description = "Provisioned NoSQL read units."
  default     = 1
}

variable "nosql_write_units" {
  type        = number
  description = "Provisioned NoSQL write units."
  default     = 1
}

variable "tags" {
  type        = map(string)
  description = "Additional freeform tags."
  default     = {}
}
