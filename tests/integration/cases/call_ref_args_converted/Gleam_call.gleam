pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_data: a, _count: b) -> Nil { Nil }

pub fn main() {
  let my_var = GList([
    GInt(1),
    GInt(2),
    GInt(3),
  ])
  let my_other = GList([
    GInt(4),
    GInt(5),
    GInt(6),
  ])
  process(my_var, GInt(42))
  process(my_other, GInt(7))
}
