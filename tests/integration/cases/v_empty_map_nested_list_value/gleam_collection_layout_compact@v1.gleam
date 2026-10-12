pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GDict([#("values", GList([GList([])]))]), GDict([])]),
    GList([GDict([]), GDict([#("values", GList([GList([])]))])]),
  ])
  let _ = my_data
}
