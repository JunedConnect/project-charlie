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

variable "public_subnets" {
  
}