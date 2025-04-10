resource "aws_lb" "test" {
  name               = "prod-alb"
  internal           = false
  load_balancer_type = "application"
  ip_address_type = "ipv4"
  security_groups    = 
  subnets            = 
  enable_deletion_protection = true
  tags = {
    Environment = "production"
  }
}

resource "aws_security_group" "alb-sg" {
  
}

resource "aws_lb" "front_end" {
  
}

resource "aws_lb" "front_end" {
  
}

resource "aws_lb_target_group" "test" {
  name     = "tf-example-lb-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}