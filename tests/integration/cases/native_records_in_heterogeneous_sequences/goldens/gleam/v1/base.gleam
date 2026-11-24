pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("h", GList([GInt(1), GStr("a"), GList([GInt(2), GStr("b")]), GDict([#("k", GList([GBool(True)]))])])),
  ])
  let _ = my_data
}
