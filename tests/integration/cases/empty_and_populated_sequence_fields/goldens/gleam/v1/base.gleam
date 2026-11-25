pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("value", GList([]))]),
    GDict([#("value", GList([GInt(1)]))]),
  ])
  let _ = my_data
}
