# Variables for Provider
variable "access_key" {
  type = string
}

variable "secret_key" {
  type = string
}

variable "region" {
  type = string
}

# Variables for S3 Storage
variable "bucket_name" {
  type = string
}


# Variables for sagemaker

variable "sagemaker_role_name" {
  type = string
}
variable "sagemaker_policy_name" {
  type = string
}

# Variables for Database Instance
variable "allocated_storage" {
  type = number
}

variable "engine" {
  type = string
}

variable "engine_version" {
  type = string
}

variable "mysql_db_name" {
  type = string
}

variable "mysql_username" {
  type = string
}
variable "mysql_password" {
  type = string
}

variable "instance_class" {
  type = string
}

variable "parameter_group_name" {
  type = string
}

variable "skip_final_snapshot" {
  type = bool
}

variable "security_group" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "identifier" {
  type = string
}

variable "publicly_accessible" {
  type = bool
}

# Ec2 Instance Variables
variable "ami" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "availability_zone" {
  type = string
}

variable "key_name" {
  type = string
}
