pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn make_widget(_value: a) -> Nil { Nil }
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GInt(42))
  let _ = consume(my_data)
}
