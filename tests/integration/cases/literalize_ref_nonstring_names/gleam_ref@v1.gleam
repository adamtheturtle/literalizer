pub type GVal {
  GNull
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let actual = GDict([
    #("_", GStr("_")),
  ])
  let my_data = GList([
    GDict([#("$ref", GInt(1))]),
    GDict([#("$ref", GNull)]),
    actual,
  ])
  let _ = my_data
}
