pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("item", GStr("existing"))]),
    // This comment describes the next item.
    GDict([#("item", GStr("next"))]),
  ])
  let _ = my_data
}
