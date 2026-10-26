pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(0b111111111111111111111111111111111111111111111111111111111111111)),
    #("b", GInt(0b1000000000000000000000000000000000000000000000000000000000000000)),
  ])
  let _ = my_data
}
