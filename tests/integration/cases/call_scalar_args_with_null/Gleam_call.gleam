pub type GVal {
  GNull
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  process(GNull)
  process(GStr("hello"))
}
