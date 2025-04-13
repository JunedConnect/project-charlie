output "LCT-SG-ID" {
    value = aws_security_group.LCT-SG.id
}

output "aws_lb_target_group-ID" {
    value = aws_lb_target_group.TCT-TG.id
}


output "vpc_id" {
  value = aws_vpc.vpc.id
}


output "subnet_ids" {
  value = [
    aws_subnet.subnet1.id,
    aws_subnet.subnet2.id,
    aws_subnet.subnet3.id
  ]
}


output "internet_gateway_id" {
  value = aws_internet_gateway.IG.id
}


output "route_table_id" {
  value = aws_route_table.RT.id
}
