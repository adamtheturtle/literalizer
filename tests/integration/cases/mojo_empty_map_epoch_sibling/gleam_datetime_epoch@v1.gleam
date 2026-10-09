pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("timestamp", GInt(1577836800))]),
    GDict([]),
  ])
  let _ = my_data
}
