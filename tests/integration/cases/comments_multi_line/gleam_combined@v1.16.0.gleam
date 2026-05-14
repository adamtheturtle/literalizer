pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    // line 1
    // line 2
    GStr("a"),
  ])
  let my_data = GList([
    // line 1
    // line 2
    GStr("a"),
  ])
  let _ = my_data
}
