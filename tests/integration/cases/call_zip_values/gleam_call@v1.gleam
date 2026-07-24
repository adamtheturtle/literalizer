pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }
pub fn emit(__call: a, __zip: b) -> Nil { Nil }

pub fn main() {
  emit(process(GStr("hello")), GInt(1))
  emit(process(GInt(42)), GInt(0))
}
