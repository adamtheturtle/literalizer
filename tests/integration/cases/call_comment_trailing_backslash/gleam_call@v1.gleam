pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GInt(1))  // trail \ .
  let _ = process(GInt(2))  // second
}
