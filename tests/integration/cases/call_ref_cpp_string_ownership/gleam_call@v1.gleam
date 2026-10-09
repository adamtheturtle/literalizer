pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let item = GStr("s")
  consume(item)
}
