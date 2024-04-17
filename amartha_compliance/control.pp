control "gcp_bucket_storage" {
  title         = "1.1 Ensure that Cloud Storage bucket is not anonymously or publicly accessible"
  description   = "It is recommended that IAM policy on Cloud Storage bucket does not allows anonymous or public access."

  tags = {
    item_id = "1.1"
    level   = "1"
    type    = "automated"
    service = "GCP/Storage"
  }

  sql = <<-EOQ
    select
      self_link resource,
      case
        when iam_policy ->> 'bindings' like any (array ['%allAuthenticatedUsers%','%allUsers%']) then 'alarm'
        else 'ok'
      end as status,
      case
        when iam_policy ->> 'bindings' like any (array ['%allAuthenticatedUsers%','%allUsers%'])
          then title || ' publicly accessible.'
        else title || ' not publicly accessible.'
      end as reason
    from
      gcp_storage_bucket;
  EOQ
}