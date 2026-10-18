pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let string_map = GDict([
    #("k", GStr("s")),
  ])
  let my_data = GList([
    string_map,
    GDict([#("k", GInt(1))]),
  ])
  let _ = my_data
}
