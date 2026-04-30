pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("$ref", GStr("ref_x"))]),
    GInt(1),
    GInt(2),
  ])
  let _ = my_data
}
