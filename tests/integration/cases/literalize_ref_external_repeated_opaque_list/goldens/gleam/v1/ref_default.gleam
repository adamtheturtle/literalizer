pub type GVal {
  GList(List(GVal))
}
pub fn consume_widget(_arg_value: a) -> Nil { Nil }

pub fn main() {
  let item = GList([])
  let my_data = GList([
    item,
    item,
  ])
  let _ = consume_widget(my_data)
}
