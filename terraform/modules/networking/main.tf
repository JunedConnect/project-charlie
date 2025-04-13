resource "aws_vpc" "cluster-charlie-vpc" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    "Name" = "${var.team_name}-VPC"
  }
}

resource "aws_internet_gateway" "cluster-charlie-vpc-igw" {
  vpc_id = aws_vpc.cluster-charlie-vpc.id
  tags = {
    Name = "${var.team_name}-VPC"
  }
}

data "aws_availability_zones" "available_zones" {}

resource "aws_subnet" "cluster-charlie-public_subnets_az1" {
  vpc_id                  = aws_vpc.cluster-charlie-vpc.id
  cidr_block              = var.public_subnet_cidr_1
  map_public_ip_on_launch = false
  availability_zone =  data.aws_availability_zones.available_zones.names[0]
  tags = {
    "Name" = "cluster-charlie-public-subnet-1"
  }
}

resource "aws_subnet" "cluster-charlie-public_subnets_az2" {
  vpc_id                  = aws_vpc.cluster-charlie-vpc.id
  cidr_block              = var.public_subnet_cidr_2
  map_public_ip_on_launch = true
  availability_zone =  data.aws_availability_zones.available_zones.names[1]
  tags = {
    "Name" = "cluster-charlie-public-subnet-2"
  }
}

resource "aws_route_table" "cluster-charlie-rt" {
  vpc_id = aws_vpc.cluster-charlie-vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.cluster-charlie-vpc-igw.id
  }
}

resource "aws_route_table_association" "cluster-charlie-rt_association-1" {
  subnet_id = aws_subnet.cluster-charlie-public_subnets_az1.id
  route_table_id = aws_route_table.cluster-charlie-rt.id
}

resource "aws_route_table_association" "cluster-charlie-rt_association-2" {
  subnet_id = aws_subnet.cluster-charlie-public_subnets_az2.id
  route_table_id = aws_route_table.cluster-charlie-rt.id
}

resource "aws_security_group" "http" {
  name   = var.aws_security_group_name
  vpc_id = aws_vpc.cluster-charlie-vpc.id
  dynamic "ingress" {
    for_each = var.sg_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

