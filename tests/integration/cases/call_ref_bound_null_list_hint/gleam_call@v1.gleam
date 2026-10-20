pub type GVal {
  GNull
  GInt(Int)
  GList(List(GVal))
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let item = GNull
  let _ = consume(item)
}
