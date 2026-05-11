pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let item_var = GDict([
    #("_", GStr("_")),
  ])
  let my_data = GDict([
    #("items", GList([item_var, GDict([#("fallback", GStr("value"))])])),
  ])
  let _ = my_data
}
