pub type GVal {
  GInt(Int)
}
pub fn make_widget(_count: a) -> Nil { Nil }

pub fn main() {
  let my_data = GInt(42)
  let my_data = make_widget(my_data)
  // note
  make_widget(my_data)
}
