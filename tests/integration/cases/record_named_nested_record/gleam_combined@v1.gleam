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
    #("lead_task", GDict([#("id", GInt(100)), #("description", GStr("first task")), #("is_done", GBool(False)), #("blocks", GList([GInt(102), GInt(103)]))])),
  ])
  let my_data = GDict([
    #("project", GStr("alpha")),
    #("lead_task", GDict([#("id", GInt(100)), #("description", GStr("first task")), #("is_done", GBool(False)), #("blocks", GList([GInt(102), GInt(103)]))])),
  ])
  let _ = my_data
}
