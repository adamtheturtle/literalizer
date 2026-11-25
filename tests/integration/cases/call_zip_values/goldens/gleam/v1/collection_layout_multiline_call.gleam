pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }
pub fn emit(_argument0: a, _argument1: b) -> Nil { Nil }

pub fn main() {
  let _ = emit(process(GStr("hello")), GBool(True))
  let _ = emit(process(GInt(42)), GBool(False))
}
