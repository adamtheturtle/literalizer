pub type GVal {
  GList(List(GVal))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let unknown_value = GList([])
  let _ = process(unknown_value)
}
