pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GDict([#("values", GList([]))]),
    GDict([]),
  ])
  let _ = my_data
}
