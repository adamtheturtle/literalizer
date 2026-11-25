pub type GVal {
  GNull
  GInt(Int)
  GList(List(GVal))
}
pub fn make_widget(_count: a) -> Nil { Nil }
pub fn consume(_count: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GNull)
  let _ = consume(my_data)
  let my_data = make_widget(GInt(42)) // note
  // extra
  let _ = consume(my_data)
}
