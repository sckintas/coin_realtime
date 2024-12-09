resource "google_project_service" "enabled_apis" {
  for_each = toset([
    "bigquery.googleapis.com",
    "storage.googleapis.com",
    "iam.googleapis.com",
    "composer.googleapis.com"
  ])
  project = var.project_id
  service = each.key
}
