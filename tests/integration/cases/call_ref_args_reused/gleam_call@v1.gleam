pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_data: a, _count: b) -> Nil { Nil }

pub fn main() {
  let single_var = GList([
    GInt(4),
    GInt(5),
    GInt(6),
  ])
  let repeated_var = GInt(1)
  process(repeated_var, GInt(1))
  process(single_var, GInt(0))
  process(repeated_var, GInt(8))
}
