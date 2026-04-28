pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(2_147_483_648)
  let _ = my_data
}
