pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([#("k", GInt(2208988800))])),
    #("b", GDict([#("k", GInt(1))])),
  ])
  let _ = my_data
}
