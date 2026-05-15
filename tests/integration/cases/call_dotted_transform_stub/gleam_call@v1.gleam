pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }
pub fn tracer_emit(__arg: a) -> Nil { Nil }

pub fn main() {
  tracer.emit(process(GStr("hello")))
  tracer.emit(process(GInt(42)))
  tracer.emit(process(GBool(True)))
}
