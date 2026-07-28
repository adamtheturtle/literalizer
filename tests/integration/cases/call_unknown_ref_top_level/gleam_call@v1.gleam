pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let unknown_value = GList([
    GInt(1),
  ])
  process(unknown_value)
}
