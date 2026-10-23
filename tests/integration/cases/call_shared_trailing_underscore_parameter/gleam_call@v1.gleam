pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_value_: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GInt(1))
}
