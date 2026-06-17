pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn record(_value: a) -> Nil { Nil }
pub fn flush(_count: a) -> Nil { Nil }

pub fn main() {
  record(GInt(42))
  flush(GInt(3))
}
