pub type GVal {
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GList([])),
    #("b", GList([])),
  ])
  let _ = my_data
}
