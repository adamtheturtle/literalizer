pub type GVal {
  GBool(Bool)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn app_mgr_run(_operation: a) -> Nil { Nil }

pub fn main() {
  app_mgr_run(GDict([#("type", GStr("create")), #("pr_id", GStr("pr_1")), #("draft", GBool(True))]))
  app_mgr_run(GDict([#("type", GStr("create")), #("pr_id", GStr("pr_2"))]))
}
