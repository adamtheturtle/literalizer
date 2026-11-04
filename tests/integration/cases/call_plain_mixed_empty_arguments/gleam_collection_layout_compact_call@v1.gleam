pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn make_widget(_before: a, _populated: b, _after: c) -> Nil { Nil }

pub fn main() {
  let _ = make_widget(GList([]), GList([GInt(1)]), GList([]))
  let _ = make_widget(GList([GStr("text")]), GList([GInt(2)]), GList([]))
  let _ = make_widget(GList([]), GList([GStr("text")]), GList([]))
  let _ = make_widget(GList([GStr("text")]), GList([GInt(2)]), GList([GInt(3)]))
}
