pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("SGVsbG8="),
    GList([]),
  ])
  let _ = my_data
}
