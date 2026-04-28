pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { panic }

pub fn main() {
  process(GInt(-1))
  process(GInt(-2))
  process(GInt(-3))
}
