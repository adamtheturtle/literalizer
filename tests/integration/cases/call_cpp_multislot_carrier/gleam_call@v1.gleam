pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a, _extra: b) -> Nil { Nil }

pub fn main() {
  process(GInt(1), GStr("hello"))
  process(GStr("two"), GBool(False))
  process(GFloat(3.5), GNull)
}
