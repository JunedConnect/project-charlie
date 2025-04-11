####Main variable 
#Networking
variable "cidr_block" {}
variable "team_name" {}
variable "public_subnets" {}
variable "aws_security_group_name" {}
variable "sg_ports" {}

# ALB
variable "alb_name" {}
variable "alb_internal" {}
variable "load_balancer_type" {}
variable "alb_ip_address_type" {}
# variable "security_groups" {}
# variable "subnets"{}
variable "listener_protocol" {}
variable "listener_port" {}
variable "redirect_status_code" {}
variable "redirect_protocol_https" {}
variable "redirect_port" {}
variable "target_group_name" {}
variable "target_group_port" {}
variable "target_group_protocol" {}