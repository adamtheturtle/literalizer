pub type GVal {
  GList(List(GVal))
}
pub fn make_widget() -> Nil { Nil }

pub fn main() {
  let my_data = make_widget()
  let _ = my_data
}
