# ALB
alb_name                        = "this"
alb_internal                    = false
alb_load_balancer_type          = "application"
listener_port_http              = "80"
listener_protocol_http          = "HTTP"
listener_port_https             = "443"
listener_protocol_https         = "HTTPS"

# ECS
ecs_cluster_name                = "this"
ecs_service_name                = "MyService"
ecs_launch_type                 = "FARGATE"
ecs_platform_version            = "LATEST"
ecs_scheduling_strategy         = "REPLICA"
ecs_desired_count               = 1
ecs_container_name              = "container"
ecs_container_port              = 5000
ecs_task_family                 = "Journaliser-TD"
ecs_task_requires_compatibilities = ["FARGATE"]
ecs_network_mode                = "awsvpc"
ecs_cpu                         = 512
ecs_memory                      = 1024
ecs_container_image             = "677276074604.dkr.ecr.eu-west-2.amazonaws.com/journal-app:latest"
ecs_container_cpu              = 256
ecs_container_memory           = 512
ecs_container_host_port        = 5000

# NETWORK
security_group_name             = "SG"
security_group_description      = "Universal"
target_group_name               = "TG"
target_group_port               = 80
target_group_protocol           = "HTTP"
target_group_target_type        = "ip"
vpc_cidr_block                  = "10.0.0.0/16"
subnet1_cidr_block              = "10.0.1.0/24"
subnet2_cidr_block              = "10.0.2.0/24"
subnet3_cidr_block              = "10.0.3.0/24"
subnet_map_public_ip_on_launch = true
subnet1_availability_zone       = "eu-west-2a"
subnet2_availability_zone       = "eu-west-2b"
subnet3_availability_zone       = "eu-west-2c"
route_cidr_block                = "0.0.0.0/0"

# ROUTE53
domain_name                     = "app.juned.co.uk"
validation_method               = "DNS"
dns_ttl                         = 60