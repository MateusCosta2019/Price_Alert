terraform {
  required_providers {
    aws = "~> 2.0"
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "price-files-all-stores"{
    bucket = "${var.bucket-name}"
    acl = "private"
    tags = {
        name = "Bucket prices SmartPhones"
        Enviroment = "Dev"
    }
}

locals {
  bucket_id = aws_s3_bucket.price-files-all-stores.id
  folders = "${var.folders}"
}

resource "aws_s3_bucket_object" "Folders" {
  count = length(local.folders)
  key   = local.folders[count.index]
  bucket = local.bucket_id
}