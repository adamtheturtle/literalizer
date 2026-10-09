pub type GVal {
  GNull
  GList(List(GVal))
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let my_null = GNull
  let regular_null = GNull
  consume(my_null)
  consume(regular_null)
}
