pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_a: a) -> Nil { Nil }

pub fn main() {
  f(GList([GList([GInt(1), GInt(2)]), GList([GInt(3)])]))
}
