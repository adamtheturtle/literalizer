pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([#("x", GInt(1))])),
    #("b", GInt(2)),
  ])
  let _ = my_data
}
