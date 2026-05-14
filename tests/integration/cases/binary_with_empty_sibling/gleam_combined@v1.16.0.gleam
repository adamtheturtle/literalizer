pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("48656c6c6f"),
    GList([]),
  ])
  let my_data = GList([
    GStr("48656c6c6f"),
    GList([]),
  ])
  let _ = my_data
}
