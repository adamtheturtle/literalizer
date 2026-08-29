pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process(_a: a) -> Nil { Nil }

pub fn main() {
  let big_list = GList([
    GStr("x"),
  ])
  process(GDict([#("m", big_list)]))
}
