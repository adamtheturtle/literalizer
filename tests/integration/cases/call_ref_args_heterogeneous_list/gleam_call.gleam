pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_data: a, _count: b) -> Nil { Nil }

pub fn main() {
  let my_ints = GList([
    GInt(1),
    GInt(2),
    GInt(3),
  ])
  let my_strings = GList([
    GStr("a"),
    GStr("b"),
  ])
  process(my_ints, GInt(42))
  process(my_strings, GInt(7))
}
