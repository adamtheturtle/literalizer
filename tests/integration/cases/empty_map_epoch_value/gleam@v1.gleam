pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("timestamp", GStr("2020-01-01T00:00:00+00:00"))]),
    GDict([]),
  ])
  let _ = my_data
}
