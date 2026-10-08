pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(1)),  // inline ending backslash \ .
    #("b", GInt(2)),
  ])
  let _ = my_data
}
