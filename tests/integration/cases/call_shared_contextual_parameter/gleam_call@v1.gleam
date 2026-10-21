pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_using: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GInt(1))
}
