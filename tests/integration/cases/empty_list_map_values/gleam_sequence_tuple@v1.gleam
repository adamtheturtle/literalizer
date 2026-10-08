pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", #(GInt(1))),
    #("b", #()),
  ])
  let _ = my_data
}
