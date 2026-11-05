pub type GVal {
  GInt(Int)
  GSet(List(GVal))
}
pub fn consume_widget(_arg_value: a) -> Nil { Nil }

pub fn main() {
  let _ = consume_widget(GSet([
    GInt(1),
    GInt(2),
  ]))
}
