pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GDict([#("$ref", GStr("my_str"))])]),
  ])
  let my_data = GList([
    GList([GDict([#("$ref", GStr("my_str"))])]),
  ])
  let _ = my_data
}
