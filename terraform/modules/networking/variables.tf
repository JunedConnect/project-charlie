variable "cidr_block" {
  type        = string
  description = "This is the cidr block for our vpc"
}

variable "team_name" {
  type        = string
  description = "The name os the dev-ops team"
}

variable "public_subnets" {
  type = list(string)
}

variable "aws_security_group_name" {
  type = string
}

variable "sg_ports" {
  type = list(number)
}

