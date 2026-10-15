pub type GVal {
  GInt(Int)
}
pub fn make_widget(_count: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GInt(0))
  let my_data = make_widget(GInt(1))
  let _ = make_widget(my_data)
}
