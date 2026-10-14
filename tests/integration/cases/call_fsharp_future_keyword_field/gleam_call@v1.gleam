pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn app_process_fetch(_data: a) -> Nil { Nil }

pub fn main() {
  let _ = app_process_fetch(GDict([#("data", GStr("hello"))]))
  let _ = app_process_fetch(GDict([#("data", GInt(42))]))
  let _ = app_process_fetch(GDict([#("data", GBool(True))]))
}
