pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("project", GStr("alpha")),
    #("lead_item", GDict([#("id", GInt(100)), #("label", GStr("first item")), #("enabled", GBool(False)), #("related_ids", GList([GInt(102), GInt(103)]))])),
  ])
  let _ = my_data
}
