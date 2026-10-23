pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([]),
    GList([GInt(1)]),
    GList([GInt(1), GInt(2)]),
    GList([GInt(1), GStr("x"), GBool(True), GNull]),
    GList([GInt(1), GInt(2), GInt(3), GInt(4), GInt(5), GInt(6), GInt(7), GInt(8)]),
  ])
  let _ = my_data
}
