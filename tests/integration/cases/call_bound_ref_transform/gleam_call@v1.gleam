pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_a: a) -> Nil { Nil }

pub fn main() {
  let ref_data = GInt(1)
  f(ref_data)
}
