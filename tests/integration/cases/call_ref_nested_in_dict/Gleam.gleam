pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GDict([#("key", GDict([#("$ref", GStr("my_var"))])), #("count", GInt(42))])]),
  ])
  let _ = my_data
}
