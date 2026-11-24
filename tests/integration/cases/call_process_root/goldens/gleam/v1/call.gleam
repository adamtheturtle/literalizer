pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process_api_fetch(_data: a) -> Nil { Nil }

pub fn main() {
  let _ = process_api_fetch(GDict([#("data", GStr("hello"))]))
  let _ = process_api_fetch(GDict([#("data", GInt(42))]))
  let _ = process_api_fetch(GDict([#("data", GBool(True))]))
}
