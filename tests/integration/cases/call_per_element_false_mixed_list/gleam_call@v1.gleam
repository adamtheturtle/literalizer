pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  process(GList([GInt(1), GStr("x")]))
}
