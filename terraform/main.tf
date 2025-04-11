module "networking" {
  source                  = "./modules/networking"
  cidr_block              = var.cidr_block
  team_name               = var.team_name
  aws_security_group_name= var.aws_security_group_name
  sg_ports = var.sg_ports
  public_subnets = var.public_subnets

}
module "ecs" {
  source = "./modules/ecs"
}

module "alb" {
  source              = "./modules/alb/"
  alb_name            = var.alb_name
  alb_internal        = var.alb_internal
  load_balancer_type  = var.load_balancer_type
  alb_ip_address_type = var.alb_ip_address_type
  security_groups = module.networking.security_groups_id
  subnets = module.networking.security_groups_id
  listener_protocol = var.listener_protocol
  listener_port = var.listener_port
  redirect_status_code = var.redirect_status_code
  redirect_protocol_https = var.redirect_protocol_https
  redirect_port = var.redirect_port
  target_group_name = var.target_group_name
  target_group_port = var.target_group_port
  target_group_protocol = var.target_group_protocol
  vpc_id = module.networking.vpc_id
}

module "r53" {
  source = "./modules/r53/"
}