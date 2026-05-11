pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a, _label: b) -> Nil { Nil }

pub fn main() {
  process(GStr("hello"), GStr("a"))
  process(GInt(42), GStr("b"))
  process(GBool(True), GStr("c"))
}
