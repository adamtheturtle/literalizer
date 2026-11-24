pub type GVal {
  GNull
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GNull)
  let _ = process(GStr("hello"))
}
