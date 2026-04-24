pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(2147483648)
  let _ = my_data
}
