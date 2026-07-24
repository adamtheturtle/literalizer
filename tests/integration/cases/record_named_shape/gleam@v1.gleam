pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("id", GInt(100)), #("label", GStr("first item")), #("enabled", GBool(False)), #("related_ids", GList([GInt(102), GInt(103)]))]),
    GDict([#("id", GInt(101)), #("label", GStr("second item")), #("enabled", GBool(True)), #("related_ids", GList([GInt(100)]))]),
  ])
  let _ = my_data
}
