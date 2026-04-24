pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(9223372036854775808)
  let _ = my_data
}
