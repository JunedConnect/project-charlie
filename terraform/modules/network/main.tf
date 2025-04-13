resource "aws_security_group" "LCT-SG" {
  name = var.security_group_name
  description = var.security_group_description
  vpc_id = aws_vpc.vpc.id

 ingress {
   from_port   = 5000
   to_port     = 5000
   protocol    = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
 }

 ingress {
   from_port   = 80
   to_port     = 80
   protocol    = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
 }

 ingress {
   from_port   = 443
   to_port     = 443
   protocol    = "tcp"
   cidr_blocks = ["0.0.0.0/0"]
 }

 egress {
   from_port   = 0
   to_port     = 0
   protocol    = -1
   cidr_blocks = ["0.0.0.0/0"]
 }
}


resource "aws_lb_target_group" "TCT-TG" {
  name        = var.target_group_name
  port        = var.target_group_port    #port 3000 or port 80 works here
  protocol    = var.target_group_protocol
  target_type = var.target_group_target_type
  vpc_id      = aws_vpc.vpc.id
}


resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr_block
}


resource "aws_subnet" "subnet1" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.subnet1_cidr_block
  map_public_ip_on_launch = var.subnet_map_public_ip_on_launch
  availability_zone       = var.subnet1_availability_zone
}


resource "aws_subnet" "subnet2" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.subnet2_cidr_block
  map_public_ip_on_launch = var.subnet_map_public_ip_on_launch
  availability_zone       = var.subnet2_availability_zone
}


resource "aws_subnet" "subnet3" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.subnet3_cidr_block
  map_public_ip_on_launch = var.subnet_map_public_ip_on_launch
  availability_zone       = var.subnet3_availability_zone
}


resource "aws_internet_gateway" "IG" {
  vpc_id = aws_vpc.vpc.id
}


resource "aws_route_table" "RT" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = var.route_cidr_block
    gateway_id = aws_internet_gateway.IG.id
  }
}


resource "aws_route_table_association" "RTA1" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.RT.id
}


resource "aws_route_table_association" "RTA2" {
  subnet_id      = aws_subnet.subnet2.id
  route_table_id = aws_route_table.RT.id
}


resource "aws_route_table_association" "RTA3" {
  subnet_id      = aws_subnet.subnet3.id
  route_table_id = aws_route_table.RT.id
}