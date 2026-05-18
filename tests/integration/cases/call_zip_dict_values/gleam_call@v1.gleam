pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process(_value: a) -> Nil { Nil }
pub fn emit(__call: a, __zip: b) -> Nil { Nil }

pub fn main() {
  emit(process(GStr("hello")), GDict([#("a", GInt(1)), #("b", GInt(2))]))
  emit(process(GInt(42)), GDict([#("c", GInt(3)), #("d", GInt(4))]))
}
