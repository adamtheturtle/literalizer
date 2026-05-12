pub type GVal {
  GBool(Bool)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("type", GStr("create")), #("pr_id", GStr("pr_1")), #("draft", GBool(True))]),
    GDict([#("type", GStr("create")), #("pr_id", GStr("pr_2"))]),
  ])
  let _ = my_data
}
