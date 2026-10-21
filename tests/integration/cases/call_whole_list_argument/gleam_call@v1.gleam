pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_a: a) -> Nil { Nil }

pub fn main() {
  let _ = f(GList([GInt(1)]))
}
