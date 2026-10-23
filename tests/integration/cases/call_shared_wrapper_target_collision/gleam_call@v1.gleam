pub type GVal {
  GInt(Int)
}
pub fn check(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = check(GInt(42))
}
