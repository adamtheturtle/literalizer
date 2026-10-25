pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn consume_widget(_arg_value: a) -> Nil { Nil }

pub fn main() {
  let shared = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = GList([
    GInt(0),
  ])
  let _ = consume_widget(my_data)
  let my_data = shared
  let _ = consume_widget(my_data)
}
