pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("b", GDict([#("k", GInt(1))])),
    #("a", GDict([#("k", GInt(2208988800))])),
  ])
  let _ = my_data
}
