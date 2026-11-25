pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn consume_widget(_arg_value: a) -> Nil { Nil }

pub fn main() {
  let _ = consume_widget(  GList([
      GInt(1),
      GInt(2),
    ]))
}
