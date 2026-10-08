pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", #(GDict([#("k", GInt(1))]))),
    #("b", #(GDict([#("k", GInt(2))]))),
  ])
  let _ = my_data
}
