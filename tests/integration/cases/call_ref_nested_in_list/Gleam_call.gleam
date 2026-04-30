pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let my_var = GInt(42)
  let my_other = GInt(7)
  process(GList([GDict([#("ref", GStr("my_var"))]), GInt(42), GStr("static")]))
  process(GList([GDict([#("ref", GStr("my_other"))]), GInt(7), GStr("label")]))
}
