pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { panic }
pub fn log_emit(__arg: a) -> Nil { panic }

pub fn main() {
  log.emit(process(GStr("hello")))
  log.emit(process(GInt(42)))
  log.emit(process(GBool(True)))
}
