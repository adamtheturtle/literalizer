pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_value: a, _count: b) -> Nil { Nil }

pub fn main() {
  process(GInt(1), GInt(42))
  process(GInt(2), GInt(100))
}
