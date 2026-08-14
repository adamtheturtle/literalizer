pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GList([GInt(1), GInt(2), GInt(3)])),  // inline a
    #("b", GInt(2)),  // inline b
  ])
  let _ = my_data
}
