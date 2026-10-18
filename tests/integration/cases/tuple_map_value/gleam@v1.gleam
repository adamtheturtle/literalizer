pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("rows", GList([GDict([#("x", GInt(1)), #("y", GStr("a"))]), GDict([#("x", GInt(2)), #("y", GStr("b"))])])),
  ])
  let _ = my_data
}
