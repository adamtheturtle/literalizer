pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(1), GStr("two")]),
    GList([]),
  ])
  let my_data = GList([
    GList([GInt(1), GStr("two")]),
    GList([]),
  ])
  let _ = my_data
}
