pub type GVal {
  GList(List(GVal))
}
pub fn make_widget(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = make_widget(GList([]))
}
