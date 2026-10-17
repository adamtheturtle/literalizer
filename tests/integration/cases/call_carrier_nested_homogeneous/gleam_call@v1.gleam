pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn app_client_go(_first_value: a, _second_value: b) -> Nil { Nil }

pub fn main() {
  let _ = app_client_go(GList([GInt(1)]), GList([GInt(2)]))
}
