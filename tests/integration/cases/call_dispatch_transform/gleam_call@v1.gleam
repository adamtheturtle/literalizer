pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn record_value(_value: a) -> Nil { Nil }
pub fn flush_buffer(_count: a) -> Nil { Nil }
pub fn emit(__arg: a) -> Nil { Nil }

pub fn main() {
  emit(record_value(GInt(42)))
  flush_buffer(GInt(3))
}
