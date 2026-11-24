pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn record_entry(_s: a, _n: b, _b: c) -> Nil { Nil }

pub fn main() {
  let my_data = record_entry(GStr("a"), GInt(1), GBool(True))
  let _ = my_data
}
