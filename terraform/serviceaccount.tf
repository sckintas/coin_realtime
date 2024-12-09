resource "google_service_account" "etl_service_account" {
  account_id   = "etl-service-account"
  display_name = "Service Account for ETL pipeline"
  project      = var.project_id
}

resource "google_project_iam_member" "service_account_roles" {
  for_each = toset([
    "roles/storage.admin",
    "roles/bigquery.admin",
    "roles/composer.worker"
  ])
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.etl_service_account.email}"
}
