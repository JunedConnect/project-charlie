#### ALB main

resource "aws_lb" "cluster-charlie-lb" {
  name                       = var.alb_name
  internal                   = var.alb_internal
  load_balancer_type         = var.load_balancer_type
  ip_address_type            = var.alb_ip_address_type
  security_groups            = var.security_groups
  subnets                    = var.public_subnet_network_azs_list
  tags = {
    Environment = "cluster-charlie"
  }
}

# resource "aws_lb_listener" "cluster-charlie-listener-http-https" {
#   depends_on = [ aws_lb.cluster-charlie-lb ]
#   load_balancer_arn = aws_lb.cluster-charlie-lb.arn
#   protocol = var.listener_protocol_http
#   port = var.listener_port_https
  
#   default_action {
#     type = "redirect" 
#     redirect {
#       status_code = var.redirect_status_code
#       protocol =  var.listener_protocol_https
#       port = var.listener_port_https
#     }

    
#   }
# }

resource "aws_lb_listener" "cluster-charlie-listener-https-https" {
  depends_on = [ aws_lb.cluster-charlie-lb ]
  load_balancer_arn = aws_lb.cluster-charlie-lb.arn
  protocol = var.listener_protocol_https
  port = var.listener_port_https
  certificate_arn = var.aws_acm_certificate
  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.cluster_charlie_tg.arn
  }
}



# variable "redirect_status_code" {
#   default = "HTTP_301"
# }
resource "aws_lb_target_group" "cluster_charlie_tg" {
  name     = var.target_group_name
  port     = var.target_group_port
  protocol = var.target_group_protocol
  vpc_id   = var.vpc_id
  target_type = var.target_type
}



# resource "aws_lb_listener" "cluster-charlie-listener-https" {
#   depends_on = [ aws_lb.cluster-charlie-lb ]
#   load_balancer_arn = aws_lb.cluster-charlie-lb.arn
#   protocol = var.listener_protocol
#   port = var.listener_port
#   default_action {
#     type = "forward"
#     target_group_arn = aws_lb_target_group.cluster_charlie_tg.arn
#   }
# }

# resource "aws_lb_target_group" "cluster_charlie_tg" {
#   name     = var.target_group_name
#   port     = var.target_group_port
#   protocol = var.target_group_protocol
#   vpc_id   = var.vpc_id
#   target_type = var.target_type
# }