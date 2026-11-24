pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_a: a, _b: b) -> Nil { Nil }

pub fn main() {
  // calls heading
  // before call one
  // first argument
  let _ = f(GInt(1), GInt(2))  // after call one
  // second argument
  let _ = f(GInt(3), GInt(4))
  // after all calls
}
