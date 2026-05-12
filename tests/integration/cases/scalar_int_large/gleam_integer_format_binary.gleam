pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(0b10000000000000000000000000000000)
  let _ = my_data
}
