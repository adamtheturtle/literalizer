pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-2147483648)),
    #("neighbor", GInt(-2147483647)),
    #("maximum", GInt(2147483647)),
    #("nested", GList([GInt(-2147483648)])),
  ])
  let _ = my_data
}
