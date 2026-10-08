pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let external_value = GInt(1)
  consume(external_value)
}
