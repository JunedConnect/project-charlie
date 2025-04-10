module "networkng" {
  source         = "./modules/networking/"
  cidr_block     = var.cidr_block
  team_name      = var.team_name
  public_subnets = var.public_subnets
}
module "ecs" {
  source = "./modules/alb"
}

module "alb" {
  source = "./modules/alb/"
  alb_name = var.alb_name
  alb_internal = var.alb_internal
  public_subnets = module.networking.public_subnets
  load_balancer_type = var.load_balancer_type
  alb_ip_address_type = var.alb_ip_address_type
  

}


module "r53" {
  source = "./modules/r53/"
}