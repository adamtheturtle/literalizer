pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(0x80000000)
  let _ = my_data
}
