pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn outer_inner(_outer: a, _n: b) -> Nil { Nil }

pub fn main() {
  outer_inner(GInt(1), GInt(2))
}
