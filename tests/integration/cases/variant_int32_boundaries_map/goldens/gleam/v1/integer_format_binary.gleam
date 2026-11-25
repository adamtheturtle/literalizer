pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("below", GInt(-{0b10000000000000000000000000000001})),
    #("minimum", GInt(-{0b10000000000000000000000000000000})),
    #("above", GInt(-{0b1111111111111111111111111111111})),
    #("nested", GList([GInt(0b0)])),
  ])
  let _ = my_data
}
