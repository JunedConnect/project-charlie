output "public_subnets_id" {
  value = [for subnet in aws_subnet.cluster-charlie-public_subnets : subnet.id]
}

output "security_groups_id" {
  value = [aws_security_group.http.id]
}

output "vpc_id" {
  value = aws_vpc.cluster-charlie-vpc.id
}