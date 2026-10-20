pub type GVal {
  GNull
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let actual = GInt(42)
  let my_data = GList([
    GDict([#("$ref", GInt(1))]),
    GDict([#("$ref", GNull)]),
    actual,
  ])
  let _ = my_data
}
