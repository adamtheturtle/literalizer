pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("first", GDict([#("items", GList([GInt(1), GDict([#("value", GInt(2))])]))])),
    #("second", GDict([#("items", GList([GInt(1), GDict([#("value", GStr("s"))])]))])),
  ])
  let _ = my_data
}
