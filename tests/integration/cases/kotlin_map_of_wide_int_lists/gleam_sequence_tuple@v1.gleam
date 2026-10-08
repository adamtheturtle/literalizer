pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", #(GInt(4294967296), GInt(4294967297))),
  ])
  let _ = my_data
}
