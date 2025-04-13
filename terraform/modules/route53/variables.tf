variable "alb_dns_name" {
  description = "Load Balancer DNS Name for network"
  type        = string
}

variable "alb_zone_id" {
  description = "Load Balancer Zone ID for network"
  type        = string
}

variable "domain_name" {
  description = "The domain name for the hosted zone"
  type        = string
}

variable "validation_method" {
  description = "The validation method for the ACM certificate"
  type        = string
}

variable "dns_ttl" {
  description = "Time to live (TTL) for DNS records"
  type        = number
}