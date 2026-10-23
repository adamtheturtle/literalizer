pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(0o52)
  // after
  let _ = my_data
}
