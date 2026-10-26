pub type GVal {
  GList(List(GVal))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let untyped_value = GList([])
  let _ = process(GList([untyped_value, untyped_value]))
}
