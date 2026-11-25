pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("2000-01-01T01:02:03"),
    GInt(1),
  ])
  let _ = my_data
}
