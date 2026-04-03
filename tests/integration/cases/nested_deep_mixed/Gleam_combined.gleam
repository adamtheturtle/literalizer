pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
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
