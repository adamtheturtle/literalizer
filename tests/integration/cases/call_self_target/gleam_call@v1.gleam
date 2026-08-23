pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn self(_value: a) -> Nil { Nil }

pub fn main() {
  self(GStr("hello"))
}
