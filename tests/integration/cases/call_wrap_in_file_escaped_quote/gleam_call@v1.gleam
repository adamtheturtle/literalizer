pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn process(_v: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GStr("a\"b"))
}
