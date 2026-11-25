pub type GVal {
  GInt(Int)
}

pub fn main() {
  let my_data = GInt(-9_223_372_036_854_775_808)
  let _ = my_data
}
