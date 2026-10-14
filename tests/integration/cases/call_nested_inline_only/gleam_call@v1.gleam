pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn f(_a: a, _b: b) -> Nil { Nil }

pub fn main() {
  let _ = f(GInt(2), GStr("hello"))  // trailing note
  let _ = f(GInt(3), GStr("world"))  // another note
}
