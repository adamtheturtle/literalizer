pub type GVal {
  GNull
  GList(List(GVal))
}
pub fn consume_widget(_arg_value: a) -> Nil { Nil }

pub fn main() {
  let item = GNull
  let my_data = GNull
  let _ = consume_widget(my_data)
  let my_data = item
  let _ = consume_widget(my_data)
}
