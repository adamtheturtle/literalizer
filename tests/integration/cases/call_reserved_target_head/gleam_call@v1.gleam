pub type GVal {
  GInt(Int)
}
pub fn class_member(_a: a) -> Nil { Nil }

pub fn main() {
  let _ = class_member(GInt(42))
}
