pub type GVal {
  GNull
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let value = GNull
  let _ = consume(value)
}
