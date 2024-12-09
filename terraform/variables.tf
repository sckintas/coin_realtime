variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region for GCP resources"
  default     = "us-central1"
  type        = string
}

variable "bucket_name" {
  description = "Name of the GCS bucket for raw data"
  default     = "coin_lake_first"
}

variable "staging_dataset" {
  description = "BigQuery staging dataset name"
  default     = "coin_stage"
}

variable "dimension_dataset" {
  description = "BigQuery dimension dataset name (post-dbt transformations)"
  default     = "coin_dim"
}
