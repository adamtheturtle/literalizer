pub type GVal {
  GStr(String)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GStr("2024-01-15"),
    GStr("2024-06-01"),
  ])
  let _ = my_data
}
