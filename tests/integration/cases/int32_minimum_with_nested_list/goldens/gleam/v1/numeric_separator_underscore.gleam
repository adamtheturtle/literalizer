pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-2_147_483_648)),
    #("neighbor", GInt(-2_147_483_647)),
    #("maximum", GInt(2_147_483_647)),
    #("nested", GList([GInt(-2_147_483_648)])),
  ])
  let _ = my_data
}
