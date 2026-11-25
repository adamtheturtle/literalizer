pub type GVal {
  GInt(Int)
}
pub fn check(_a: a) -> Nil { Nil }

pub fn main() {
  let _ = check(GInt(42))
}
