variable "compartment_id" {
  type        = string
  description = "OCI compartment OCID."
}

variable "region" {
  type        = string
  description = "OCI region."
  default     = "ap-osaka-1"
}

variable "environment" {
  type        = string
  description = "Environment name."
}

variable "bucket_suffix" {
  type        = string
  description = "Globally unique bucket suffix."
}

variable "name_prefix" {
  type    = string
  default = "digital-technical"
}

variable "vcn_cidr" {
  type    = string
  default = "10.42.0.0/16"
}

variable "subnet_cidr" {
  type    = string
  default = "10.42.10.0/24"
}

variable "nosql_read_units" {
  type    = number
  default = 1
}

variable "nosql_write_units" {
  type    = number
  default = 1
}

variable "tags" {
  type    = map(string)
  default = {}
}
