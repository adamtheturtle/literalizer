pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-{0o20000000000})),
    #("neighbor", GInt(-{0o17777777777})),
    #("maximum", GInt(0o17777777777)),
    #("nested", GList([GInt(-{0o20000000000})])),
  ])
  let _ = my_data
}
