###ECS MAIN 
resource "aws_ecs_cluster" "cluster_charlie_ecs_cluster" {
  name = var.ecs_cluster_name
  
}

resource "aws_ecs_service" "cluster_charlie_ecs_service" {
  depends_on = [ 
    aws_ecs_cluster.cluster_charlie_ecs_cluster,
    aws_ecs_task_definition.cluster_charlie_task
  ]
  name = var.ecs_service_name 
  launch_type = var.ecs_launch_type
  platform_version =  var.platform_version
  cluster =  aws_ecs_cluster.cluster_charlie_ecs_cluster.id
  task_definition = aws_ecs_task_definition.cluster_charlie_task.id
  desired_count = var.desired_count
  # availability_zone_rebalancing = var.az_zone_rebalancing

  load_balancer {
    target_group_arn = var.target_group_arn
    container_name =  var.ecs_container_name
    container_port = var.ecs_container_port
  }
  network_configuration {
    subnets = var.public_subnet_network_azs_list
    security_groups = var.security_groups_id
    assign_public_ip = true
  }

}

resource "aws_ecs_task_definition" "cluster_charlie_task" {
  family = "cluster-charlie-project"
  requires_compatibilities = [var.compatibilities]
  task_role_arn = aws_iam_role.ecs_task_execution_role.arn
  cpu = var.task_cpu
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  memory = var.task_memory
  network_mode = var.ecs_network_mode
  container_definitions = jsonencode([
    {
      name      = var.ecs_container_name
      image     = var.container_image_name
      cpu       = var.ecs_task_container_cpu
      memory    = var.ecs_task_container_memory
      essential = true
      portMappings = [
        {
          containerPort = var.ecs_container_port
          hostPort      = var.ecs_container_port
        }
      ]
    }
  ])
}



resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Effect    = "Allow"
        Sid       = ""
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  role       = aws_iam_role.ecs_task_execution_role.name
}

resource "aws_iam_role_policy_attachment" "ecs_execution_policy_attachment_2" {
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
  role       = aws_iam_role.ecs_task_execution_role.name
}