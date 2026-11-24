pub type GVal {
  GStr(String)
}

pub fn main() {
  let my_data = GStr("hello # world")  // note
  let _ = my_data
}
