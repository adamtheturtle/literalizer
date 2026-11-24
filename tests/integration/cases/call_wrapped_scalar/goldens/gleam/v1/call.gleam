pub type GVal {
  GInt(Int)
}
pub fn make_widget(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = make_widget(GInt(1))
}
