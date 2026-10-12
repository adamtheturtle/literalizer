pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let item = GList([
    GInt(1),
    GInt(2),
  ])
  process(GList([item, item]))
}
