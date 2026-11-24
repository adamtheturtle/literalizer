pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let shared = GList([
    GList([GInt(1), GInt(2)]),
    GDict([#("value", GInt(1))]),
  ])
  let my_data = GList([
    shared,
    shared,
  ])
  let _ = my_data
}
