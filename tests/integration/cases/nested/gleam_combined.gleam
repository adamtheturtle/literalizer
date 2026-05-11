pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("users", GList([GDict([#("name", GStr("Bob")), #("tags", GList([GStr("admin"), GStr("user")]))]), GDict([#("name", GStr("Carol")), #("tags", GList([GStr("guest")]))])])),
  ])
  let my_data = GDict([
    #("users", GList([GDict([#("name", GStr("Bob")), #("tags", GList([GStr("admin"), GStr("user")]))]), GDict([#("name", GStr("Carol")), #("tags", GList([GStr("guest")]))])])),
  ])
  let _ = my_data
}
