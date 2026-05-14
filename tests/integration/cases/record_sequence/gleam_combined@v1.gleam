pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("id", GInt(1)), #("label", GStr("first"))]),
    GDict([#("id", GInt(2)), #("label", GStr("second"))]),
    GDict([#("id", GInt(3)), #("label", GStr("third"))]),
  ])
  let my_data = GList([
    GDict([#("id", GInt(1)), #("label", GStr("first"))]),
    GDict([#("id", GInt(2)), #("label", GStr("second"))]),
    GDict([#("id", GInt(3)), #("label", GStr("third"))]),
  ])
  let _ = my_data
}
