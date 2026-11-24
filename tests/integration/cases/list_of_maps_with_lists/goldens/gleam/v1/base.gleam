pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("a", GList([GInt(1)]))]),
    GDict([#("a", GList([GInt(2)]))]),
  ])
  let _ = my_data
}
