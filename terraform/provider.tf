terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.94.1"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

# terraform {
#   backend "s3" {
#     bucket = "" 
#     key = ""
#     # use_lockfile = false
#     region = "value"
#   }
# }

