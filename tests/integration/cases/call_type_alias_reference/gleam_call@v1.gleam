pub type GVal {
  GInt(Int)
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  let value = GInt(1)
  let _ = process(value)
}
