pub type GVal {
  GInt(Int)
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let shared = GInt(42)
  let _ = consume(shared)
}
