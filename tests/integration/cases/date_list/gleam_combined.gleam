pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("2024-01-15"),
    GStr("2024-02-20"),
  ])
  let my_data = GList([
    GStr("2024-01-15"),
    GStr("2024-02-20"),
  ])
  let _ = my_data
}
