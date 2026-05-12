pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("name", GStr("Alice")),
    #("scores", GList([GInt(10), GInt(20), GInt(30)])),
  ])
  let _ = my_data
}
