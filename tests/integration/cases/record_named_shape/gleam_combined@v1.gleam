pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("id", GInt(100)), #("description", GStr("first task")), #("is_done", GBool(False)), #("blocks", GList([GInt(102), GInt(103)]))]),
    GDict([#("id", GInt(101)), #("description", GStr("second task")), #("is_done", GBool(True)), #("blocks", GList([GInt(100)]))]),
  ])
  let my_data = GList([
    GDict([#("id", GInt(100)), #("description", GStr("first task")), #("is_done", GBool(False)), #("blocks", GList([GInt(102), GInt(103)]))]),
    GDict([#("id", GInt(101)), #("description", GStr("second task")), #("is_done", GBool(True)), #("blocks", GList([GInt(100)]))]),
  ])
  let _ = my_data
}
