pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("a"),
    // trailing
  ])
  let my_data = GList([
    GStr("a"),
    // trailing
  ])
  let _ = my_data
}
