pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GDict([#("b", GList([GInt(1), GInt(2), GInt(3)]))])),
  ])
  let _ = my_data
}
