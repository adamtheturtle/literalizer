pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    // first
    GStr("a"),
    // second
    GStr("b"),
  ])
  let my_data = GList([
    // first
    GStr("a"),
    // second
    GStr("b"),
  ])
  let _ = my_data
}
