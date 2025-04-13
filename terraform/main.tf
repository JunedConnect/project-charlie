module "networking" {
  source                  = "./modules/networking"
  cidr_block              = var.cidr_block
  team_name               = var.team_name
  aws_security_group_name = var.aws_security_group_name
  sg_ports                = var.sg_ports
  availability_zone       = var.availability_zone
  public_subnet_cidr_1    = var.public_subnet_cidr_1
  public_subnet_cidr_2    = var.public_subnet_cidr_2


}
module "alb" {
  depends_on                     = [module.networking]
  source                         = "./modules/alb/"
  alb_name                       = var.alb_name
  alb_internal                   = var.alb_internal
  load_balancer_type             = var.load_balancer_type
  alb_ip_address_type            = var.alb_ip_address_type
  security_groups                = module.networking.security_groups_id
  listener_protocol_http              = var.listener_protocol_http
  listener_port_http                  = var.listener_port_http
  redirect_status_code           = var.redirect_status_code
  redirect_protocol_https        = var.redirect_protocol_https
  redirect_port                  = var.redirect_port
  target_group_name              = var.target_group_name
  target_group_port              = var.target_group_port
  target_group_protocol          = var.target_group_protocol
  vpc_id                         = module.networking.vpc_id
  public_subnet_network_azs_list = module.networking.public_subnets
  target_type = var.target_type
  aws_acm_certificate = module.r53.aws_acm_certificate
  listener_port_https = var.listener_port_https
  listener_protocol_https = var.listener_protocol_https
}

module "ecs" {
  source                         = "./modules/ecs"
  ecs_cluster_name               = var.ecs_cluster_name
  ecs_service_name               = var.ecs_service_name
  ecs_launch_type                = var.ecs_launch_type
  platform_version               = var.platform_version
  desired_count                  = var.desired_count
  elb_name                       = module.alb.elb_name
  target_group_arn               = module.alb.target_group_arn
  ecs_container_name             = var.ecs_container_name
  ecs_container_port             = var.ecs_container_port
  public_subnet_network_azs_list = module.networking.public_subnets
  compatibilities                = var.compatibilities
  task_cpu                       = var.task_cpu
  task_memory                    = var.task_memory
  ecs_network_mode               = var.ecs_network_mode
  security_groups_id = module.networking.security_groups_id
  ecs_task_container_cpu = var.ecs_task_container_cpu
  ecs_task_container_memory = var.ecs_task_container_memory
  container_image_name = var.container_image_name
}


module "r53" {
  source = "./modules/r53/"
  validation_method = var.validation_method
  dns_ttl = var.dns_ttl
  alb_dns_name = module.alb.alb_dns_name
  alb_zone_id = module.alb.alb_zone_id
  app_subdomain = var.app_subdomain
  hosted_zone_domain_name  = var.hosted_zone_domain_name
}

