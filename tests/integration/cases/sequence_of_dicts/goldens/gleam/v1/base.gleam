pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("name", GStr("Alice")), #("age", GInt(30))]),
    GDict([#("name", GStr("Bob")), #("age", GInt(25))]),
  ])
  let _ = my_data
}
