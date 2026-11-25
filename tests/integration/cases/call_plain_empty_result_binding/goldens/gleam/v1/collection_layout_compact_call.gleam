pub type GVal {
  GList(List(GVal))
}
pub fn make_widget(_value: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GList([]))
  let _ = my_data
}
