pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GStr("a\"b")]),
  ])
  let _ = my_data
}
