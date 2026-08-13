pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("ts", GInt(32535215999)),
  ])
  let _ = my_data
}
