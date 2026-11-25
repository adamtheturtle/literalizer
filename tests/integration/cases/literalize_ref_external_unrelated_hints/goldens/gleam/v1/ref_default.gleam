pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn consume_widget(_arg_value: a) -> Nil { Nil }

pub fn main() {
  let missing = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = missing
  let _ = consume_widget(my_data)
}
