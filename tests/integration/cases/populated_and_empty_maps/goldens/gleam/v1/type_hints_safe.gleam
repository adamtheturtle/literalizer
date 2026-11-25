pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("a", GInt(1))]),
    GDict([]),
  ])
  let _ = my_data
}
