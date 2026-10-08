pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-{0x80000000})),
    #("below", GInt(-{0xb2d05e00})),
  ])
  let _ = my_data
}
