pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_a: a) -> Nil { Nil }

pub fn main() {
  let _ = f(#(#(GInt(1), GInt(2)), #(GInt(3))))
}
