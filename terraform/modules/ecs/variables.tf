####ECS Variables
variable "ecs_cluster_name" {
  description = "The Name of the ECS Cluster"
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

variable "security_groups_id" {
  description = "Security groups id "
}
variable "elb_name" {
  description = "Name of the ELB"
}
variable "target_group_arn" {
  description = "The ARN for the target group"
}


variable "ecs_container_name" {
  description = "Name of the ecs container"
}

variable "ecs_container_port" {
  description = "Port of the ecs container"
}

variable "public_subnet_network_azs_list" {
  description = "List of subnet id"
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

