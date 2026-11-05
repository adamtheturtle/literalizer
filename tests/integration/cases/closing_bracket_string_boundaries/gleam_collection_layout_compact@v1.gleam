pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("]"),
    GStr("a]"),
    GStr("a]="),
    GStr("a]b"),
  ])
  let _ = my_data
}
