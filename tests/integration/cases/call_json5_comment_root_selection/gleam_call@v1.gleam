pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_a: a, _b: b) -> Nil { Nil }

pub fn main() {
  // selected heading
  let _ = f(GInt(1), GInt(2))  // selected inline
}
