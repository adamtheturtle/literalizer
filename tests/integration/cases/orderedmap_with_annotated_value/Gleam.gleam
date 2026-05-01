pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GList([])),
    #("b", GInt(1)),
  ])
  let _ = my_data
}
