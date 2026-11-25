pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_using: a) -> Nil { Nil }

pub fn main() {
  let _ = f(GInt(1))
}
