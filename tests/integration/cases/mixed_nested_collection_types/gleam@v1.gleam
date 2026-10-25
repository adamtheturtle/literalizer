pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("lists", GList([GList([GInt(1)]), GList([GStr("x")]), GList([])])),
    #("maps", GList([GDict([#("x", GInt(1))]), GDict([#("x", GStr("s"))])])),
    #("empties", GDict([#("a", GList([GInt(1)])), #("b", GList([]))])),
  ])
  let _ = my_data
}
