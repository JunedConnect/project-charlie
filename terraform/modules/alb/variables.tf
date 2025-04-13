##### ALB MODULE
variable "alb_name" {
  description = "The Name of the Application Load Balancer"
}
variable "alb_internal" {
  description = "Public facing or Private loadbalance"
}
variable "load_balancer_type" {
  description = "Type of Load Balancer"
}
variable "alb_ip_address_type" {
  description = "ip address type of load balancer"
}
variable "public_subnet_network_azs_list"{}
variable "security_groups" {}
variable "listener_protocol_http" {}
variable "listener_port_http" {}
variable "redirect_status_code" {}
variable "redirect_protocol_https" {}
variable "redirect_port" {}
variable "target_group_name" {}
variable "target_group_port" {}
variable "target_group_protocol" {}
variable "vpc_id" {}
variable "target_type" {}
variable "aws_acm_certificate" {}

variable "listener_protocol_https" {}

variable "listener_port_https" {}
