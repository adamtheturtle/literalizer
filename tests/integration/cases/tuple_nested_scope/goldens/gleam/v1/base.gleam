pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("x", GList([GInt(1), GList([GInt(2), GList([GInt(3)])])])),
  ])
  let _ = my_data
}
