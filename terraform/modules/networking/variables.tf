
### Networking VAriables 
variable "cidr_block" {
  type        = string
  description = "This is the cidr block for our vpc"
}

variable "team_name" {
  type        = string
  description = "The name os the dev-ops team"
}


variable "aws_security_group_name" {
  type = string
}

variable "sg_ports" {
  type = list(number)
}
variable "public_subnet_cidr_1" {}
variable "public_subnet_cidr_2" {}
variable "availability_zone" {}

