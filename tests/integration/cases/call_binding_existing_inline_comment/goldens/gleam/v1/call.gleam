pub type GVal {
  GInt(Int)
}
pub fn make_widget(_count: a) -> Nil { Nil }
pub fn consume_widget(_count: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GInt(42))
  let _ = consume_widget(my_data)
  let my_data = make_widget(GInt(42)) // note
  let _ = consume_widget(my_data)
}
