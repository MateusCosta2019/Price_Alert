terraform {
  required_providers {
    aws = "~> 2.0"
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "magazine-luiza-data-files-prices"{
    bucket = "magazine-luiza-data-files-prices"
    tags = {
        name = "Bucket MagazineLuiza"
        Enviroment = "Prod"
    }
}

locals {
  bucket_id = aws_s3_bucket.magazine-luiza-data-files-prices.id
  folders = ["Raw/", "Trusted/", "Refined/"]
}

resource "aws_s3_bucket_object" "Folders" {
  count = length(local.folders)
  key   = local.folders[count.index]
  bucket = local.bucket_id
}