pub type GVal {
  GInt(Int)
}
pub fn make_widget(_value: a) -> Nil { Nil }

pub fn main() {
  let value = GInt(1)
  let _ = make_widget(value)
}
