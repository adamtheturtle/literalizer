pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GStr("09:30:00"))
  let _ = process(GStr("2024-01-15T00:00:00+00:00"))
  let _ = process(GInt(1))
}
