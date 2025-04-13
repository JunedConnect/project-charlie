module "alb" {
    source = "./modules/alb"
    security_group_id = module.network.LCT-SG-ID
    target_group_id = module.network.aws_lb_target_group-ID
    certificate_arn = module.route53.certificate_arn
    subnets = module.network.subnet_ids

    alb_name                     = var.alb_name
    alb_internal                 = var.alb_internal
    alb_load_balancer_type       = var.alb_load_balancer_type
    listener_port_http           = var.listener_port_http
    listener_protocol_http       = var.listener_protocol_http
    listener_port_https          = var.listener_port_https
    listener_protocol_https      = var.listener_protocol_https  
}

module "ecs" {
    source = "./modules/ecs"
    security_group_id = module.network.LCT-SG-ID
    target_group_id = module.network.aws_lb_target_group-ID
    subnets = module.network.subnet_ids

    ecs_cluster_name               = var.ecs_cluster_name
    ecs_service_name               = var.ecs_service_name
    ecs_launch_type                = var.ecs_launch_type
    ecs_platform_version           = var.ecs_platform_version
    ecs_scheduling_strategy        = var.ecs_scheduling_strategy
    ecs_desired_count              = var.ecs_desired_count
    ecs_container_name             = var.ecs_container_name
    ecs_container_port             = var.ecs_container_port
    ecs_task_family                = var.ecs_task_family
    ecs_task_requires_compatibilities = var.ecs_task_requires_compatibilities
    ecs_network_mode               = var.ecs_network_mode
    ecs_cpu                        = var.ecs_cpu
    ecs_memory                     = var.ecs_memory
    ecs_container_image            = var.ecs_container_image
    ecs_container_cpu              = var.ecs_container_cpu
    ecs_container_memory           = var.ecs_container_memory
    ecs_container_host_port        = var.ecs_container_host_port
}

module "network" {
    source = "./modules/network"
    vpc_id = module.network.vpc_id

    security_group_name              = var.security_group_name
    security_group_description       = var.security_group_description
    target_group_name                = var.target_group_name
    target_group_port                = var.target_group_port
    target_group_protocol            = var.target_group_protocol
    target_group_target_type         = var.target_group_target_type
    vpc_cidr_block                   = var.vpc_cidr_block
    subnet1_cidr_block               = var.subnet1_cidr_block
    subnet2_cidr_block               = var.subnet2_cidr_block
    subnet3_cidr_block               = var.subnet3_cidr_block
    subnet_map_public_ip_on_launch   = var.subnet_map_public_ip_on_launch
    subnet1_availability_zone        = var.subnet1_availability_zone
    subnet2_availability_zone        = var.subnet2_availability_zone
    subnet3_availability_zone        = var.subnet3_availability_zone
    route_cidr_block                 = var.route_cidr_block
}

module "route53" {
    source = "./modules/route53"
    alb_dns_name = module.alb.LCT-ALB-DNS
    alb_zone_id = module.alb.LCT-ALB-ZONE-ID

    domain_name          = var.domain_name
    validation_method    = var.validation_method
    dns_ttl              = var.dns_ttl
}