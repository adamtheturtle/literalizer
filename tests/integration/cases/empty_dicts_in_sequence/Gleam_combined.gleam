pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([]),
    GDict([]),
  ])
  let my_data = GList([
    GDict([]),
    GDict([]),
  ])
  let _ = my_data
}
