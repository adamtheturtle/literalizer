pub type GVal {
  GNull
  GInt(Int)
  GList(List(GVal))
}
pub fn make_widget(_count: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GNull)
  let my_data = make_widget(GInt(42)) // note
}
