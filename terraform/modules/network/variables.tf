variable "vpc_id" {
  description = "VPC ID for resources that require it"
  type        = string
}

variable "security_group_name" {
  description = "Name of the security group"
  type        = string
}

variable "security_group_description" {
  description = "Description of the security group"
  type        = string
}

variable "target_group_name" {
  description = "Name of the target group"
  type        = string
}

variable "target_group_port" {
  description = "Port for the target group"
  type        = number
}

variable "target_group_protocol" {
  description = "Protocol for the target group"
  type        = string
}

variable "target_group_target_type" {
  description = "Target type for the target group"
  type        = string
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "subnet1_cidr_block" {
  description = "CIDR block for subnet 1"
  type        = string
}

variable "subnet2_cidr_block" {
  description = "CIDR block for subnet 2"
  type        = string
}

variable "subnet3_cidr_block" {
  description = "CIDR block for subnet 3"
  type        = string
}

variable "subnet_map_public_ip_on_launch" {
  description = "Whether to map public IP on launch for subnets"
  type        = bool
}

variable "subnet1_availability_zone" {
  description = "Availability zone for subnet 1"
  type        = string
}

variable "subnet2_availability_zone" {
  description = "Availability zone for subnet 2"
  type        = string
}

variable "subnet3_availability_zone" {
  description = "Availability zone for subnet 3"
  type        = string
}

variable "route_cidr_block" {
  description = "CIDR block for the route"
  type        = string
}