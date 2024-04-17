benchmark "amartha_compliance" {
  title         = "Amartha Security Posture v1.0"
  children = [
    benchmark.amartha_compliance_1
  ]

  tags = {
    type    = "Benchmark"
    service = "Amartha"
    category = "Compliance"
  }
}

benchmark "amartha_compliance_1" {
  title         = "1. Storage"
  children = [
    control.gcp_bucket_storage
  ]

  tags = {
    type    = "Benchmark"
    service = "Amartha"
    category = "Compliance"
  }
}