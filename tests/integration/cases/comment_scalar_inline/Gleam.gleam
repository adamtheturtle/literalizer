pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(42)  // note
  let _ = my_data
}
