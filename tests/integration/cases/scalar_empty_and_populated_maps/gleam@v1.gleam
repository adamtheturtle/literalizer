pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GInt(1),
    GDict([]),
    GDict([#("x", GInt(2))]),
  ])
  let _ = my_data
}
