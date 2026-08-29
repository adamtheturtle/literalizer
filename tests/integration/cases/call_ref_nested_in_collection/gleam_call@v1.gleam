pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process(_a: a, _b: b) -> Nil { Nil }

pub fn main() {
  let big_list = GList([
    GStr("x"),
  ])
  process(GDict([#("k", big_list)]), GInt(2))
}
