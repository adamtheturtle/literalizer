pub type GVal {
  GStr(String)
}
pub fn make_widget(_text: a) -> Nil { Nil }

pub fn main() {
  let my_data = make_widget(GStr("first \"quote\"\n// string body")) // note
  // extra
  let _ = my_data
}
