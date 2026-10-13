pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a, _label: b) -> Nil { Nil }

pub fn main() {
  let _ = process(GStr("hello"), GStr("a"))
  let _ = process(GInt(42), GStr("b"))
  let _ = process(GBool(True), GStr("c"))
}
