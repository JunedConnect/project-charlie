variable "hosted_zone_domain_name" {
  description = "Name of the R53 domain"
}

variable "app_subdomain" {
  
}

variable "validation_method" {
  description = "DNS used to validate the domain "
}

variable "dns_ttl" {
  description = "Time to live (TTL) for DNS records"
}
variable "alb_dns_name" {
  
}

variable "alb_zone_id" {
  
}

