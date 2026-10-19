pub type GVal {
  GInt(Int)
}
pub fn thing_first_value(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = thing_first_value(GInt(1))
}
