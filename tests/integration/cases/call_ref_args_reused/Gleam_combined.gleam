pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GList([
    GList([GDict([#("$ref", GStr("repeated_var"))]), GInt(1)]),
    GList([GDict([#("$ref", GStr("single_var"))]), GInt(0)]),
    GList([GDict([#("$ref", GStr("repeated_var"))]), GInt(8)]),
  ])
  let my_data = GList([
    GList([GDict([#("$ref", GStr("repeated_var"))]), GInt(1)]),
    GList([GDict([#("$ref", GStr("single_var"))]), GInt(0)]),
    GList([GDict([#("$ref", GStr("repeated_var"))]), GInt(8)]),
  ])
  let _ = my_data
}
