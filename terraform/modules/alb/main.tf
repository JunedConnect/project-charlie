#### ALB main

resource "aws_lb" "cluster-charlie-lb" {
  name                       = var.alb_name
  internal                   = var.alb_internal
  load_balancer_type         = var.load_balancer_type
  ip_address_type            = var.alb_ip_address_type
  security_groups            = var.security_groups
  subnets                    = var.subnets
  enable_deletion_protection = true
  tags = {
    Environment = "cluster-charlie"
  }
}

# ### forward just in case we forward to https to https connection so secure connection from end user to our backend 
# resource "aws_lb_listener" "cluster-charlie-listener-https-https" {
#   depends_on = [ aws_lb.cluster-charlie-lb ]
#   load_balancer_arn = aws_lb.cluster-charlie-lb.arn
#   protocol = var.redirect_protocol_https
#   port = var.listener_port
#   # certificate_arn = #### need to create certificate for this to work asked juned
#   default_action {
#     type = "forward"
#     forward {
#       target_group {
#         arn = aws_lb_target_group.cluster-charlie-tg.arn
#       }
#     }
#   }

# }


resource "aws_lb_listener" "cluster-charlie-listener-https-http" {
  depends_on = [ aws_lb.cluster-charlie-lb ]
  load_balancer_arn = aws_lb.cluster-charlie-lb.arn
  protocol = var.listener_protocol
  port = var.listener_port
  default_action {
    type = "redirect"
    redirect {
      protocol = var.redirect_protocol_https
      status_code = var.redirect_status_code
      port = var.redirect_port
    }
  }
}

resource "aws_lb_target_group" "test" {
  name     = var.target_group_name
  port     = var.target_group_port
  protocol = var.target_group_protocol
  vpc_id   = var.vpc_id
}