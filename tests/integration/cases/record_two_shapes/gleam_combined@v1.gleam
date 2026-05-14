pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("user", GDict([#("id", GInt(1)), #("name", GStr("Alice"))])),
    #("project", GDict([#("title", GStr("report")), #("tags", GList([GStr("draft"), GStr("urgent")]))])),
  ])
  let my_data = GDict([
    #("user", GDict([#("id", GInt(1)), #("name", GStr("Alice"))])),
    #("project", GDict([#("title", GStr("report")), #("tags", GList([GStr("draft"), GStr("urgent")]))])),
  ])
  let _ = my_data
}
