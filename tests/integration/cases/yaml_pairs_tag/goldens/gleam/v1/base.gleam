pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("first", GInt(1))]),
    GDict([#("repeated", GStr("a"))]),
    GDict([#("repeated", GStr("b"))]),
  ])
  let _ = my_data
}
