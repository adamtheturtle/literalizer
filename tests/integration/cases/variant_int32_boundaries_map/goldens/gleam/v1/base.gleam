pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("below", GInt(-2147483649)),
    #("minimum", GInt(-2147483648)),
    #("above", GInt(-2147483647)),
    #("nested", GList([GInt(0)])),
  ])
  let _ = my_data
}
