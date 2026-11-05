pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // first dotted key
    // second dotted key
    #("a", GDict([#("b", GInt(1)), #("c", GInt(2))])),
  ])
  let _ = my_data
}
