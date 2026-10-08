pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", #(#(GInt(1), GInt(2)))),
    #("b", #(#(GInt(3)))),
  ])
  let _ = my_data
}
