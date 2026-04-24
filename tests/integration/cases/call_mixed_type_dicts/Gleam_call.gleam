pub type GVal {
  GBool(Bool)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn app_mgr_op(_operation: a) -> Nil { panic }

pub fn main() {
  app_mgr_op(GDict([#("type", GStr("create")), #("pr_id", GStr("pr_1")), #("draft", GBool(True))]))
  app_mgr_op(GDict([#("type", GStr("create")), #("pr_id", GStr("pr_2"))]))
}
