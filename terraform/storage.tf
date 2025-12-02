# Main bucket for everything (project data, etc.)
resource "google_storage_bucket" "project-bucket" {
  name    = "batch-2170-political-reality-check"
  project = data.google_project.project.name

  location = local.location

  force_destroy = true

  hierarchical_namespace {
    enabled = true
  }

  soft_delete_policy {
    retention_duration_seconds = 604800
  }
}
