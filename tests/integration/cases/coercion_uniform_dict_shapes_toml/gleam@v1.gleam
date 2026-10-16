pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("_", GList([GDict([#("type", GStr("create")), #("name", GStr("a"))]), GDict([#("type", GStr("update")), #("name", GStr("b"))])])),
  ])
  let _ = my_data
}
