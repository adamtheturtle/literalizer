pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn f(_a: a, _b: b) -> Nil { Nil }

pub fn main() {
  f(GInt(2), GStr("hello"))  // trailing note
  f(GInt(3), GStr("world"))  // another note
}
