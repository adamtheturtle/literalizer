pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("below", GInt(-{0x80000001})),
    #("minimum", GInt(-{0x80000000})),
    #("above", GInt(-{0x7fffffff})),
    #("nested", GList([GInt(0x0)])),
  ])
  let _ = my_data
}
