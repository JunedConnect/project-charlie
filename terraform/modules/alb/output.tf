output "elb_name" {
  value = aws_lb.cluster-charlie-lb.id
}

output "target_group_arn" {
  value = aws_lb_target_group.cluster_charlie_tg.id
}

output "alb_dns_name" {
  value = aws_lb.cluster-charlie-lb.dns_name
}

output "alb_zone_id" {
  value = aws_lb.cluster-charlie-lb.zone_id
}
