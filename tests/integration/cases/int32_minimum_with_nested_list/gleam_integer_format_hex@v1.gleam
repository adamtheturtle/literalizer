pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("minimum", GInt(-{0x80000000})),
    #("neighbor", GInt(-{0x7fffffff})),
    #("maximum", GInt(0x7fffffff)),
    #("nested", GList([GInt(-{0x80000000})])),
  ])
  let _ = my_data
}
