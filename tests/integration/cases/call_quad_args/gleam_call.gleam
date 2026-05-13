pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_a: a, _b: b, _c: c, _d: d) -> Nil { Nil }

pub fn main() {
  process(GInt(1), GInt(2), GInt(3), GInt(4))
  process(GInt(5), GInt(6), GInt(7), GInt(8))
}
