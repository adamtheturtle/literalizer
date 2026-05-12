pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("key", GStr("hello   world")), #("value", GInt(1))]),
  ])
  let my_data = GList([
    GDict([#("key", GStr("hello   world")), #("value", GInt(1))]),
  ])
  let _ = my_data
}
