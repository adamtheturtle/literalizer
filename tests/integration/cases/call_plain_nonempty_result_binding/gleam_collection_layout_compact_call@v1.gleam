pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn make_widget(_value: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GList([GInt(1)]))
  let _ = my_data
}
