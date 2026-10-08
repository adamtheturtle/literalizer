pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("groups", #(#(GDict([#("id", GInt(1))])), #(GDict([#("id", GInt(2))])))),
  ])
  let _ = my_data
}
