module "networkng" {
  source = "./modules/networking/"
  cidr_block = var.cidr_block
  team_name = var.team_name
  public_subnets = var.public_subnets
}

module "alb" {
  source = "./modules/alb/"

}

module "ecs" {
  source = "./modules/alb"
}

module "r53" {
  source = "./modules/r53/"
}