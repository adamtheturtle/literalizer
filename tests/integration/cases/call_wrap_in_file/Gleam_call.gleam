pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_a: a, _b: b) -> Nil { Nil }

pub fn main() {
  process(GInt(1), GInt(2))
  process(GInt(3), GInt(4))
}
