pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GList([GList([GInt(1)]), GList([GInt(2)])])),
    #("b", GList([GList([GStr("x")]), GList([GStr("y")])])),
  ])
  let _ = my_data
}
