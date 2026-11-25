pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_xs: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GList([
    GInt(1),
    GInt(2),
  ]))
  let _ = process(GList([
    GInt(3),
  ]))
}
