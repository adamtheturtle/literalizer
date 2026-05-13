pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_int = GInt(42)
  let my_data = my_int
  let _ = my_data
}
