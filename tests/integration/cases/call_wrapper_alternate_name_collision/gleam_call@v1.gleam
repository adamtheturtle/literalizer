pub type GVal {
  GInt(Int)
}
pub fn check_wrapper(_a: a) -> Nil { Nil }

pub fn main() {
  let _ = check_wrapper(GInt(42))
}
