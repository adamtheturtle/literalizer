pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn consume_widget(_arg_value: a) -> Nil { Nil }

pub fn main() {
  let a = GInt(0)
  let my_data = GList([
    a,
    GInt(1),
  ])
  let _ = consume_widget(my_data)
}
