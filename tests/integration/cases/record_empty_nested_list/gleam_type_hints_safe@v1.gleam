pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GList([GList([GInt(1), GInt(2)]), GList([GInt(3)])])),
    #("b", GList([GList([]), GList([GInt(1)])])),
  ])
  let _ = my_data
}
