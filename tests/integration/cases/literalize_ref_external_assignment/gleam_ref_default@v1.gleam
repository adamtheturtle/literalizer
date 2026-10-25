pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn consume_widget(_arg_value: a) -> Nil { Nil }

pub fn main() {
  let ref_data = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = GList([
    GInt(0),
  ])
  let _ = consume_widget(my_data)
  let my_data = ref_data
  let _ = consume_widget(my_data)
}
