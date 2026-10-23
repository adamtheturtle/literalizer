pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(0x1)),
    #("b", GInt(0x10000000000)),
  ])
  let _ = my_data
}
