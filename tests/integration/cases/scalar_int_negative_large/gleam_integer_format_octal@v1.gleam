pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(-{0o20000000001})
  let _ = my_data
}
