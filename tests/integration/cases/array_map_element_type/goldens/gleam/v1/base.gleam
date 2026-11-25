pub type GVal {
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("d", GList([GDict([#("a", GList([GDict([#("b", GList([GInt(1), GList([GFloat(2.5), GList([GStr("x"), GList([GBool(True)])])])]))])]))])])),
  ])
  let _ = my_data
}
