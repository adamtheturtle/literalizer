pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("nested", GDict([#("count", GInt(1)), #("name", GStr("value"))]))]),
    GDict([]),
  ])
  let _ = my_data
}
