pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let my_var = GInt(42)
  let my_other = GInt(7)
  let _ = process(GList([my_var, GInt(42), GStr("static")]))
  let _ = process(GList([my_other, GInt(7), GStr("label")]))
}
