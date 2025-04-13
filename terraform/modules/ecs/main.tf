resource "aws_ecs_cluster" "TCT-Cluster" {
  name = var.ecs_cluster_name

}


resource "aws_ecs_service" "TCD-Service" {
  name                               = var.ecs_cluster_name
  launch_type                        = var.ecs_launch_type
  platform_version                   = var.ecs_platform_version
  cluster                            = aws_ecs_cluster.TCT-Cluster.id
  task_definition                    = aws_ecs_task_definition.TCD-TD.id
  scheduling_strategy                = var.ecs_scheduling_strategy
  desired_count                      = var.ecs_desired_count

  network_configuration {
    assign_public_ip = true
    security_groups  = [var.security_group_id]
    subnets          = var.subnets
  }


  load_balancer {
    target_group_arn = var.target_group_id
    container_name   = var.ecs_container_name
    container_port   = var.ecs_container_port
  }
}


resource "aws_ecs_task_definition" "TCD-TD" {
  family                   = var.ecs_task_family
  requires_compatibilities = var.ecs_task_requires_compatibilities
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  network_mode             = var.ecs_network_mode
  cpu                      = var.ecs_cpu
  memory                   = var.ecs_memory
  container_definitions = jsonencode([
    {
      name      = "container"
      image     = var.ecs_container_image
      cpu       = var.ecs_container_cpu
      memory    = var.ecs_container_memory
      essential = true
      portMappings = [
        {
          containerPort = var.ecs_container_port
          hostPort      = var.ecs_container_host_port
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

resource "aws_iam_role_policy_attachment" "ecs_execution_policy_attachment2" {
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
  role       = aws_iam_role.ecs_task_execution_role.name
}