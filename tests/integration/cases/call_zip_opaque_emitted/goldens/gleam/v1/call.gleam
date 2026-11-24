pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }
pub fn emit(_argument0: a, _argument1: b) -> Nil { Nil }

pub fn main() {
  let _ = emit(process(GInt(1)), GStr("2024-01-15T12:00:00"))
}
