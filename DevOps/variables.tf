variable "aws_region" {
  default = "us-west-2"
}

# S3 Buckets
variable "folders" {
  default = ["Raw/", "Trusted/", "Refined/"]
}
variable "bucket-name" {
  default = "price-files-all-stores"
}