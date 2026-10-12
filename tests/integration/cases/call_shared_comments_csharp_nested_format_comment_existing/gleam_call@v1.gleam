pub type GVal {
  GNull
  GInt(Int)
  GList(List(GVal))
}
pub fn make_widget(_count: a) -> Nil { Nil }

pub fn main() {
  let my_data = GNull
  let my_data = ($"{$"{1://}"}").Length >= 0 ? make_widget(GInt(42)) : make_widget(GInt(42)) // trailing
  // extra
}
