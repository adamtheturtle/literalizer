pub type GVal {
  GList(List(GVal))
}
pub fn make_widget(_value: a) -> Nil { Nil }

pub fn main() {
  let items = GList([])
  let _ = make_widget(items)
}
