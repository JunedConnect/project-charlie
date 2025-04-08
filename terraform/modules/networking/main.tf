resource "aws_vpc" "charlie-prod-vpc" {
  cidr_block = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support = true
  tags = {
    "Name" = "${var.team_name}-VPC"
  }
}

resource "aws_internet_gateway" "charlie-prod-vpc-igw" {
  vpc_id = aws_vpc.charlie-prod-vpc.id
  tags = {
    Name = "${var.team_name}-VPC"
  }
}

resource "aws_subnet" "charlie-prod_public_subnets" {
  for_each = { for idx, cidr in var.public_subnets : idx => cidr }
  vpc_id = aws_vpc.charlie-prod-vpc.id
  cidr_block = each.value
  map_public_ip_on_launch = true
  tags = {
    "Name" = "public-subnet-${each.key}"
  }
}

resource "aws_route_table" "charlie-prod_rt" {
  vpc_id = aws_vpc.charlie-prod-vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.charlie-prod-vpc-igw.id
  }
}

resource "aws_route_table_association" "charlie-prod_rt_association" {
  for_each = aws_subnet.charlie-prod_public_subnets
  subnet_id      = each.value.id
  route_table_id = aws_route_table.charlie-prod_rt.id
}