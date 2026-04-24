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
pub fn app_mgr_op(_operation: a) -> Nil { panic }

pub fn main() {
  app_mgr_op(GDict([#("type", GStr("create")), #("pr_id", GStr("pr_1")), #("draft", GBool(True))]))
  app_mgr_op(GDict([#("type", GStr("create")), #("pr_id", GStr("pr_2"))]))
}
