pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GStr("time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)"))
}
