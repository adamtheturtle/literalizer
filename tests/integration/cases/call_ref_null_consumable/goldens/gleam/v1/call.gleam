pub type GVal {
  GNull
  GList(List(GVal))
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let my_null = GNull
  let regular_null = GNull
  let _ = consume(my_null)
  let _ = consume(regular_null)
}
