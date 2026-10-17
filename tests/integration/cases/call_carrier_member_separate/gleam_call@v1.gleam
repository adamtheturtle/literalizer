pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn app_go(_first_value: a, _second_value: b) -> Nil { Nil }

pub fn main() {
  let _ = app_go(GList([GInt(1)]), GList([GStr("text")]))
}
