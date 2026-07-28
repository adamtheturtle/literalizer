pub type GVal {
  GList(List(GVal))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let known_value = GInt(1)
  let unknown_value = GList([])
  process(unknown_value)
}
