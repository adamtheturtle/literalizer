pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([])),
    #("b", GInt(1)),
  ])
  let _ = my_data
}
