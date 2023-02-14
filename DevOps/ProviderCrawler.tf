variable "database_name" {
  default = "s3://magazine-luiza-data-files-prices/Raw/"
}

resource "aws_glue_catalog_database" "database" {
  name = "Raw-Catalog"

  create_table_default_permission {
    permission = ["SELECT"]
    principal {
        data_lake_principal_identifier = "IAM_ALLOWED_PRINCIPALS"
    }
  }
}

resource "aws_glue_crawler" "raw-crawler" {
  database_name = aws_glue_catalog_database.database.name
  name = "raw-crawler"

  s3_target {
    path = "${database_name}"
  }
  tags = {
    "Raw" = "raw-data-crawler"
  }
}