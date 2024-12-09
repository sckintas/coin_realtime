resource "google_composer_environment" "composer_env" {
  name    = "etl-composer-env"
  project = var.project_id
  region  = var.region

  config {
    software_config {
      image_version = "composer-2.9.11-airflow-2.10.2" # Example supported version
    }
  }
}
