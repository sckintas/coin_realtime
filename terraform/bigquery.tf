resource "google_bigquery_dataset" "staging_dataset" {
  dataset_id                 = var.staging_dataset
  project                    = var.project_id
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "dimension_dataset" {
  dataset_id                 = var.dimension_dataset
  project                    = var.project_id
  location                   = var.region
  delete_contents_on_destroy = true
}
