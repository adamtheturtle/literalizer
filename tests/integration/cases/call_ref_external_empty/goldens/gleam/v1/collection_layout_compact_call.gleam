pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let item = GList([
    GInt(1),
    GInt(2),
  ])
  let _ = consume(item)
}
