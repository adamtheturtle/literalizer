pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GStr("hello"))
  let _ = process(GInt(42))
  let _ = process(GBool(True))
}
