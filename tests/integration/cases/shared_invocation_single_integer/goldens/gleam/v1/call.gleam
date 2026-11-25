pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = consume(GInt(1))
}
