pub type GVal {
  GInt(Int)
}
pub fn make_widget(_count: a) -> Nil { Nil }

pub fn main() {
  let my_data = (~/\//).match("/") ? make_widget(GInt(42)) : null // trailing
  let _ = my_data
}
