pub type GVal {
  GStr(String)
}
pub fn make_widget(_text: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GStr("text"))
  let _ = my_data
}
