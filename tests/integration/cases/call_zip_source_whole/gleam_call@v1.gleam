pub type GVal {
  GBool(Bool)
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }
pub fn emit(__call: a, __zip: b) -> Nil { Nil }

pub fn main() {
  emit(process(GInt(42)), GBool(True))
}
