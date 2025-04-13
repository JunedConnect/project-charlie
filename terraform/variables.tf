####Main variable 
#Networking
variable "cidr_block" {}
variable "team_name" {}
variable "public_subnet_cidr_1" {}
variable "public_subnet_cidr_2" {}
variable "aws_security_group_name" {}
variable "sg_ports" {}
variable "availability_zone" {}

# ALB
variable "alb_name" {}
variable "alb_internal" {}
variable "load_balancer_type" {}
variable "alb_ip_address_type" {}
variable "listener_protocol_http" {}
# variable "listener_port" {}
variable "redirect_status_code" {}
variable "redirect_protocol_https" {}
variable "redirect_port" {}
variable "target_group_name" {}
variable "target_group_port" {}
variable "target_group_protocol" {}
variable "target_type" {}


variable "listener_protocol_https" {
  
}

variable "listener_port_https" {
  
}

variable "listener_port_http" {
  
}



#ECS

variable "ecs_cluster_name" {
  description = "The name of the ECS cluster "
}
variable "ecs_service_name" {
  description = "The name of the ECS Service"
}

variable "ecs_launch_type" {
  description = "The type of ECS service we want "
}

variable "platform_version" {
  description = "The Platform version on which to run your service."
}

variable "desired_count" {
  description = "Number of instances of the task definition to place and keep running"
}

# variable "az_zone_rebalancing" {
#   description = "automatically redistributes tasks within a service across Availability Zones (AZs) to mitigate the risk of impaired application availability"
# }

variable "ecs_container_name" {
  description = "Name of the ecs container"
}

variable "ecs_container_port" {
  description = "Port of the ecs container"
}

variable "compatibilities" {
  description = "compatibilities requirement for our task"
}

variable "task_cpu" {
  description = "The task CPU ammount"
}

variable "task_memory" {
  description = "The task memory amount"
}
variable "ecs_network_mode" {
  description = "Docker networking mode to use for the containers in the task."
}

variable "ecs_task_container_memory" {
  
}

variable "ecs_task_container_cpu" {
  
}

variable "container_image_name" {
  
}

# variable "container_name" {
  
# }


###R53

variable "validation_method" {
  description = "DNS used to validate the domain "
}

variable "dns_ttl" {
  description = "Time to live (TTL) for DNS records"
}

variable "hosted_zone_domain_name" {
  description = "Name of the R53 domain"
}

variable "app_subdomain" {
  
}