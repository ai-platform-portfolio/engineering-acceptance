module "identity" {
  source = "git::https://github.com/ai-platform-portfolio/terraform-modules.git//modules/identity?ref=30b25adaee96f7589bb8bd575b03ab2177b62b8a"

  resource_group_name = "acceptance-only"
  location            = "uksouth"
  name_prefix         = "acceptance"
  loc_short           = "uks"
  oidc_issuer_url     = "https://issuer.example.invalid"
  workloads          = {}
}
