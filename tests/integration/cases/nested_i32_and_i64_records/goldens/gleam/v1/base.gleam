pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GDict([#("value", GInt(1))])]),
    GList([GDict([#("value", GInt(1099511627776))])]),
  ])
  let _ = my_data
}
