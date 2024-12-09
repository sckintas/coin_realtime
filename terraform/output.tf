output "bucket_name" {
  description = "Name of the GCS bucket"
  value       = google_storage_bucket.data_lake.name
}

output "staging_dataset" {
  description = "ID of the BigQuery staging dataset"
  value       = google_bigquery_dataset.staging_dataset.dataset_id
}

output "dimension_dataset" {
  description = "ID of the BigQuery dimension dataset"
  value       = google_bigquery_dataset.dimension_dataset.dataset_id
}

output "service_account_email" {
  description = "Service Account Email"
  value       = google_service_account.etl_service_account.email
}
