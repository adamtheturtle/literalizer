pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("a"),
    //
    GStr("b"),
  ])
  let _ = my_data
}
