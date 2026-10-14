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
  let _ = process(GInt(1), GStr("hello"))
  let _ = process(GStr("two"), GBool(False))
  let _ = process(GFloat(3.5), GNull)
}
