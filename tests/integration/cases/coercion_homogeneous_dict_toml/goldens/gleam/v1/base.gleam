pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("_", GDict([#("a", GInt(1)), #("b", GInt(2))])),
  ])
  let _ = my_data
}
