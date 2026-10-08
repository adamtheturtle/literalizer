pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_value: a) -> Nil { Nil }

pub fn main() {
  f(GList([GInt(1), GInt(2)]))
}
