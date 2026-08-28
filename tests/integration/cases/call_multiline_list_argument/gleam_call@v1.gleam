pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_xs: a) -> Nil { Nil }

pub fn main() {
  process(GList([
    GInt(1),
    GInt(2),
  ]))
  process(GList([
    GInt(3),
  ]))
}
