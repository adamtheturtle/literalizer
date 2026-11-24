pub type GVal {
  GInt(Int)
  GFloat(Float)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(0b1)),
    #("b", GFloat(2.5)),
    #("c", GInt(0b11)),
  ])
  let _ = my_data
}
