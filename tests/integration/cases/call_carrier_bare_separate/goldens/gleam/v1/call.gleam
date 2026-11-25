pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn make_widget(_first_value: a, _second_value: b) -> Nil { Nil }

pub fn main() {
  let _ = make_widget(GList([GInt(1)]), GList([GStr("text")]))
}
