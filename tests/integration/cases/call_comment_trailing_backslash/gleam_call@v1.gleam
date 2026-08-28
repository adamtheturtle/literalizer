pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  process(GInt(1))  // trail \ .
  process(GInt(2))  // second
}
