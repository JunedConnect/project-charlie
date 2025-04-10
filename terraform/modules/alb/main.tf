resource "aws_lb" "charlie-lb" {
  name               = var.alb_name
  internal           = var.alb_internal
  load_balancer_type = var.load_balancer_type
  ip_address_type    = var.alb_ip_address_type
  security_groups    = [] ## TODO
  subnets            = 
  enable_deletion_protection = true
  tags = {
    Environment = "production"
  }
}

resource "aws_lb_listener" "name" {
  
}

resource "aws_lb_target_group" "test" {
  name     = "tf-example-lb-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}