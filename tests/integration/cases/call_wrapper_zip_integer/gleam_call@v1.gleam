pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }
pub fn emit(_argument0: a, _argument1: b) -> Nil { Nil }

pub fn main() {
  let _ = emit(process(GInt(1)), GInt(42))
}
