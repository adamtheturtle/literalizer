pub type GVal {
  GStr(String)
}

pub fn main() {
  let my_data = GStr("\u{0000}x")
  let _ = my_data
}
