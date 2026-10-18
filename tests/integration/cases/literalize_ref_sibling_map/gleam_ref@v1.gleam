pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let sibling_map = GDict([
    #("k", GInt(2)),
  ])
  let my_data = GList([
    GDict([#("k", GInt(1))]),
    sibling_map,
  ])
  let _ = my_data
}
