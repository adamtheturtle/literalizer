pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn make_widget(_before: a, _populated: b, _after: c) -> Nil { Nil }

pub fn main() {
  let _ = make_widget(#(), #(GInt(1)), #())
  let _ = make_widget(#(GStr("text")), #(GInt(2)), #())
  let _ = make_widget(#(), #(GStr("text")), #())
  let _ = make_widget(#(GStr("text")), #(GInt(2)), #(GInt(3)))
}
