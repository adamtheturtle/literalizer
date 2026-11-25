pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([]),
    GList([GInt(1), GStr("value")]),
    GList([GInt(2), GInt(3)]),
  ])
  let _ = my_data
}
