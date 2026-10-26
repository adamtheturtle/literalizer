pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn make_widget(_first: a, _second: b) -> Nil { Nil }
pub fn consume(_first: a, _second: b) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GInt(42), GInt(3))
  let _ = consume(my_data, GInt(3))
}
