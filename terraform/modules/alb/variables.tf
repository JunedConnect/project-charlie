variable "security_group_id" {
  description = "Security Group ID for ALB"
  type        = string
}

variable "target_group_id" {
  description = "Target Group ID for ALB"
  type        = string
}

variable "certificate_arn" {
  description = "ARN of the ACM certificate for ALB"
  type        = string
}

variable "subnets" {
  description = "List of subnet IDs where the ALB will be deployed"
  type        = list(string)
}

variable "alb_name" {
  description = "Name of the Application Load Balancer"
  type        = string
}

variable "alb_internal" {
  description = "Whether the ALB is internal or not"
  type        = bool
}

variable "alb_load_balancer_type" {
  description = "Type of the load balancer"
  type        = string
}

variable "listener_port_http" {
  description = "Port for the HTTP listener"
  type        = string
}

variable "listener_protocol_http" {
  description = "Protocol for the HTTP listener"
  type        = string
}

variable "listener_port_https" {
  description = "Port for the HTTPS listener"
  type        = string
}

variable "listener_protocol_https" {
  description = "Protocol for the HTTPS listener"
  type        = string
}