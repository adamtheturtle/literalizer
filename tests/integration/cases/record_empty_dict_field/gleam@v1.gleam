pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("f", GDict([])),
    #("g", GInt(1)),
  ])
  let _ = my_data
}
