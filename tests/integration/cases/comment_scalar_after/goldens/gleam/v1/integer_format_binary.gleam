pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(0b101010)
  // after
  let _ = my_data
}
