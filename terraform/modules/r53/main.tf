data "aws_route53_zone" "existing_zone" {
  name = var.hosted_zone_domain_name
}

resource "aws_acm_certificate" "cluster_charlie_cert" {
  domain_name       = var.app_subdomain
  validation_method = var.validation_method
  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_route53_record" "cert_validation_record" {
  for_each = {
    for dvo in aws_acm_certificate.cluster_charlie_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  zone_id = data.aws_route53_zone.existing_zone.zone_id
  name    = each.value.name
  type    = each.value.type
  ttl     = 60
  records = [each.value.record]
}

# cert_validation_record = 
resource "aws_acm_certificate_validation" "cert_validation" {
  certificate_arn         = aws_acm_certificate.cluster_charlie_cert.arn
  validation_record_fqdns = [
    for record in aws_route53_record.cert_validation_record :
    record.fqdn
  ]
}


resource "aws_route53_record" "alb_record" {
  zone_id = data.aws_route53_zone.existing_zone.zone_id
  name    = var.app_subdomain
  type    = "A"
  alias {
    name                   = var.alb_dns_name
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }
}

