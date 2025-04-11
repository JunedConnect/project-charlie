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

variable "security_groups" {}
variable "subnets"{}
variable "listener_protocol" {}
variable "listener_port" {}
variable "redirect_status_code" {}
variable "redirect_protocol_https" {}
variable "redirect_port" {}
variable "target_group_name" {}
variable "target_group_port" {}
variable "target_group_protocol" {}
variable "vpc_id" {}