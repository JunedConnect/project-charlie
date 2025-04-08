module "networkng" {
  source = "./modules/networking/"
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