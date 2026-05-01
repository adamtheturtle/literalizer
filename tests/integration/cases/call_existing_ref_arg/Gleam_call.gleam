pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn send(_value: a) -> Nil { Nil }

pub fn main() {
  let existing = GInt(42)
  send(existing)
}
