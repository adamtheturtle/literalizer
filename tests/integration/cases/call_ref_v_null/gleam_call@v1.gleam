pub type GVal {
  GNull
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let value = GNull
  consume(value)
}
