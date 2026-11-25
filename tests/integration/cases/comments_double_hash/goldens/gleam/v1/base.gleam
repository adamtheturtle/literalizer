pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    // # section
    GStr("a"),
  ])
  let _ = my_data
}
