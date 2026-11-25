pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("first", GDict([#("x", GInt(1)), #("y", GInt(2))])),
    #("second", GDict([#("z", GInt(3))])),
  ])
  let _ = my_data
}
