pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("below", GInt(-{0o20000000001})),
    #("minimum", GInt(-{0o20000000000})),
    #("above", GInt(-{0o17777777777})),
    #("nested", GList([GInt(0o0)])),
  ])
  let _ = my_data
}
