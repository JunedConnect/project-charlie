variable "security_group_id" {
  description = "Security Group ID for ECS"
  type        = string
}

variable "target_group_id" {
  description = "Target Group ID for ECS"
  type        = string
}

variable "subnets" {
  description = "List of subnet IDs where the ECS service will run"
  type        = list(string)
}

variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  type        = string
}

variable "ecs_service_name" {
  description = "Name of the ECS service"
  type        = string
}

variable "ecs_launch_type" {
  description = "Launch type for the ECS service"
  type        = string
}

variable "ecs_platform_version" {
  description = "Platform version for the ECS service"
  type        = string
}

variable "ecs_scheduling_strategy" {
  description = "Scheduling strategy for the ECS service"
  type        = string
}

variable "ecs_desired_count" {
  description = "Desired count for ECS service tasks"
  type        = number
}

variable "ecs_container_name" {
  description = "Name of the ECS container"
  type        = string
}

variable "ecs_container_port" {
  description = "Container port for ECS service"
  type        = number
}

variable "ecs_task_family" {
  description = "Task family for ECS task definition"
  type        = string
}

variable "ecs_task_requires_compatibilities" {
  description = "The compatibility requirements for the ECS task definition (e.g., FARGATE or EC2)"
  type        = list(string)
}

variable "ecs_network_mode" {
  description = "Network mode for ECS task"
  type        = string
}

variable "ecs_cpu" {
  description = "CPU units for ECS task"
  type        = number
}

variable "ecs_memory" {
  description = "Memory (in MiB) for ECS task"
  type        = number
}

variable "ecs_container_image" {
  description = "Docker image for ECS container"
  type        = string
}

variable "ecs_container_cpu" {
  description = "CPU units for the ECS container"
  type        = number
}

variable "ecs_container_memory" {
  description = "Memory (in MiB) for ECS container"
  type        = number
}

variable "ecs_container_host_port" {
  description = "Host port for the ECS container"
  type        = number
}