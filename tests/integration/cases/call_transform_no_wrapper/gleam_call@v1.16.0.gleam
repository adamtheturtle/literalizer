pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  process(GStr("hello"))
  process(GInt(42))
  process(GBool(True))
}
