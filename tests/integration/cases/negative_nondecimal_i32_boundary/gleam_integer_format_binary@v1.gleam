pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-{0b10000000000000000000000000000000})),
    #("below", GInt(-{0b10110010110100000101111000000000})),
  ])
  let _ = my_data
}
