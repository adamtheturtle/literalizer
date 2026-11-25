pub type GVal {
  GList(List(GVal))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let untyped_value = #()
  let _ = process(#(untyped_value, untyped_value))
}
