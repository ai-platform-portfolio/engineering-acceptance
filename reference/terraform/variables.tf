variable "workloads" {
  type = map(object({
    namespace = string
    sa_name   = string
  }))
  default = {}
}
