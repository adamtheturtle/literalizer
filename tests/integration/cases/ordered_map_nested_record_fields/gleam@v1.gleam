pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("first", GDict([#("x", GInt(1))])),
    #("second", GDict([#("y", GInt(2))])),
  ])
  let _ = my_data
}
