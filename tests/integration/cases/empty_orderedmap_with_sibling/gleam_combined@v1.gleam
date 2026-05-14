pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([]),
    GList([]),
  ])
  let my_data = GList([
    GDict([]),
    GList([]),
  ])
  let _ = my_data
}
