pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(42)
  // after
  let _ = my_data
}
