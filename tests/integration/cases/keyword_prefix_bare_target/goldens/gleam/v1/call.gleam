pub type GVal {
  GInt(Int)
}
pub fn first_value(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = first_value(GInt(1))
}
