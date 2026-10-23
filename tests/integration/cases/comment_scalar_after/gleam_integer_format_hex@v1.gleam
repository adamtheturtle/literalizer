pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(0x2a)
  // after
  let _ = my_data
}
