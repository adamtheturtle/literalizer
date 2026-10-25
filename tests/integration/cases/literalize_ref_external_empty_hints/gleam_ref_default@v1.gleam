pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn consume_widget(_arg_value: a) -> Nil { Nil }

pub fn main() {
  let item = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = GList([
    GInt(1),
    GInt(2),
  ])
  let _ = consume_widget(my_data)
  let my_data = item
  let _ = consume_widget(my_data)
}
