pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  // Test cases
  process(GDict([#("type", GStr("create")), #("pr_id", GStr("pr_1"))]))  // first case
  process(GDict([#("type", GStr("update")), #("pr_id", GStr("pr_2"))]))  // second case
  // third case
  process(GDict([#("type", GStr("delete")), #("pr_id", GStr("pr_3"))]))
}
