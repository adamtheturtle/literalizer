pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_a: a, _b: b, _c: c, _d: d) -> Nil { Nil }

pub fn main() {
  process(GInt(1), GInt(2), GInt(3), GInt(4))
  process(GInt(10), GInt(20), GInt(30), GInt(40))
}
