pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GList([GInt(1), GInt(2)]), GList([GStr("a"), GStr("b")])]),
  ])
  let my_data = GList([
    GList([GList([GInt(1), GInt(2)]), GList([GStr("a"), GStr("b")])]),
  ])
  let _ = my_data
}
