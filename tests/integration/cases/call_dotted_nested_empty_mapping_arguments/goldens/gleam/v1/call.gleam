pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn api_worker_process(_values: a, _count: b) -> Nil { Nil }

pub fn main() {
  let _ = api_worker_process(GList([GInt(1), GDict([])]), GInt(42))
  let _ = api_worker_process(GList([GInt(2), GDict([#("x", GStr("s"))])]), GInt(43))
}
