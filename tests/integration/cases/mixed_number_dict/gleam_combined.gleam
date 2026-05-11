pub type GVal {
  GInt(Int)
  GFloat(Float)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(1)),
    #("b", GFloat(2.5)),
    #("c", GInt(3)),
  ])
  let my_data = GDict([
    #("a", GInt(1)),
    #("b", GFloat(2.5)),
    #("c", GInt(3)),
  ])
  let _ = my_data
}
