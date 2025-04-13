output "public_subnets" {
  value = [
    aws_subnet.cluster-charlie-public_subnets_az1.id,
    aws_subnet.cluster-charlie-public_subnets_az2.id
  ]
}
output "security_groups_id" {
  value = [aws_security_group.http.id]
  
}

output "vpc_id" {
  value = aws_vpc.cluster-charlie-vpc.id
}