pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_int = GInt(42)
  let my_data = my_int
  let _ = my_data
}
