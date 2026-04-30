pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GList([GDict([#("$ref", GStr("my_var"))]), GInt(42), GStr("static")])]),
    GList([GList([GDict([#("$ref", GStr("my_other"))]), GInt(7), GStr("label")])]),
  ])
  let my_data = GList([
    GList([GList([GDict([#("$ref", GStr("my_var"))]), GInt(42), GStr("static")])]),
    GList([GList([GDict([#("$ref", GStr("my_other"))]), GInt(7), GStr("label")])]),
  ])
  let _ = my_data
}
