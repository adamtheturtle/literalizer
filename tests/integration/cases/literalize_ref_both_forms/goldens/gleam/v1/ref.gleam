pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let shared_values = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = GDict([
    #("a", shared_values),
  ])
  let _ = my_data
  let my_data = GDict([
    #("a", shared_values),
  ])
  let _ = my_data
}
