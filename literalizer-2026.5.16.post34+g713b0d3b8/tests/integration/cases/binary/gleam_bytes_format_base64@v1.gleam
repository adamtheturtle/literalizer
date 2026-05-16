pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("SGVsbG8="),
  ])
  let _ = my_data
}
