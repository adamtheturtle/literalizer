pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GDict([#("type", GStr("create")), #("pr_id", GStr("pr_1")), #("draft", GBool(True))]),
    GDict([#("type", GStr("create")), #("pr_id", GStr("pr_2"))]),
  ])
  let my_data = GList([
    GDict([#("type", GStr("create")), #("pr_id", GStr("pr_1")), #("draft", GBool(True))]),
    GDict([#("type", GStr("create")), #("pr_id", GStr("pr_2"))]),
  ])
  let _ = my_data
}
