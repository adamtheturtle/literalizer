pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let shared = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = GDict([
    #("a", shared),
  ])
  let my_data = GDict([
    #("a", shared),
  ])
  let _ = my_data
}
