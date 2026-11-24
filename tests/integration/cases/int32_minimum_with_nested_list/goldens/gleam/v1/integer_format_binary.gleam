pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-{0b10000000000000000000000000000000})),
    #("neighbor", GInt(-{0b1111111111111111111111111111111})),
    #("maximum", GInt(0b1111111111111111111111111111111)),
    #("nested", GList([GInt(-{0b10000000000000000000000000000000})])),
  ])
  let _ = my_data
}
