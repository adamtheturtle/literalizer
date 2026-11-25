pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_a: a) -> Nil { Nil }
pub fn repr(_argument0: a) -> Nil { Nil }

pub fn main() {
  let ref_data = GInt(1)
  let _ = repr(f(ref_data))
}
