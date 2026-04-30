pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GList([GDict([#("$ref", GStr("myVar"))]), GInt(42), GStr("static")])]),
  ])
  let _ = my_data
}
