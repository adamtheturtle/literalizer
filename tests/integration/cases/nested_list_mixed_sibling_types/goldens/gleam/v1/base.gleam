pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(1), GInt(2)]),
    GList([]),
    GList([GStr("a"), GStr("b")]),
  ])
  let _ = my_data
}
