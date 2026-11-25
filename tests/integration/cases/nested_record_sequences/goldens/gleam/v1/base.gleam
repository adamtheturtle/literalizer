pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GDict([#("a", GInt(1))])]),
    GList([GDict([#("a", GInt(2))])]),
  ])
  let _ = my_data
}
