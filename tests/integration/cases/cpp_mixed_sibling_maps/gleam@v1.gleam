pub type GVal {
  GNull
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GDict([#("a", GInt(1))]), GDict([#("a", GNull)]), GInt(42)]),
    GList([GDict([#("a", GInt(1))]), GDict([#("a", GStr("s"))]), GInt(42)]),
    GList([GDict([#("a", GInt(1))]), GDict([#("a", GNull)])]),
    GList([GDict([#("a", GInt(1))]), GDict([#("a", GStr("s"))])]),
  ])
  let _ = my_data
}
