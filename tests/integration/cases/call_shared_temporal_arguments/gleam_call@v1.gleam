pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn check(_timestamp: a, _date_value: b) -> Nil { Nil }

pub fn main() {
  let _ = check(GStr("2024-01-15T10:30:00+00:00"), GStr("2024-06-01"))
}
