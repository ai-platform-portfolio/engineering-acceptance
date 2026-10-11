module "identity" {
  source = "git::https://github.com/ai-platform-portfolio/platform-iac.git//terraform/modules/azure/identity?ref=041965b358d7196eafb6fafca5587e4710d1d16e"

  resource_group_name = "acceptance-only"
  location            = "uksouth"
  name_prefix         = "acceptance"
  loc_short           = "uks"
  oidc_issuer_url     = "https://issuer.example.invalid"
  workloads           = var.workloads
}
