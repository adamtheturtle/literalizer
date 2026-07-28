pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  process(GStr("09:30:00"))
  process(GStr("2024-01-15T00:00:00+00:00"))
  process(GInt(1))
}
