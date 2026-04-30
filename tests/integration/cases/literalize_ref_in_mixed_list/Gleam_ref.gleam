pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let x = GDict([
    #("_", GStr("_")),
  ])
  let my_data = GList([
    x,
    GInt(1),
    GInt(2),
  ])
  let _ = my_data
}
