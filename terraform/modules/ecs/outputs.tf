output "TCT-Cluster-ID" {
    value = aws_ecs_service.TCD-Service.id
}

output "TCD-Service-ID" {
    value = aws_ecs_cluster.TCT-Cluster.id
}

output "TCD-TD-ID" {
    value = aws_ecs_task_definition.TCD-TD.id
}