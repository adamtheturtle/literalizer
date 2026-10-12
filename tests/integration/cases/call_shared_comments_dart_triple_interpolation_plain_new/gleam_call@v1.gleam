pub type GVal {
  GInt(Int)
}
pub fn make_widget(_count: a) -> Nil { Nil }

pub fn main() {
  let my_data = ('''prefix ${'// payload'}''').length >= 0 ? make_widget(GInt(42)) : make_widget(GInt(42))
  let _ = my_data
}
