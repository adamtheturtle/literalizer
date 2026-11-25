pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn make_widget(_items: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GList([GList([GInt(1), GInt(2)]), GList([GInt(3)])]))
  let _ = my_data
}
