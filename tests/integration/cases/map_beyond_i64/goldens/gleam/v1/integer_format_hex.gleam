pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GInt(0x7fffffffffffffff)),
    #("b", GInt(0x8000000000000000)),
  ])
  let _ = my_data
}
