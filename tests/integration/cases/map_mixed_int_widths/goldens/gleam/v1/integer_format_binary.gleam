pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(0b1)),
    #("b", GInt(0b10000000000000000000000000000000000000000)),
  ])
  let _ = my_data
}
