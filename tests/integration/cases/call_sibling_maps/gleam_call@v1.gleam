pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  process(GDict([#("value", GInt(1))]))
  process(GDict([#("value", GStr("hello"))]))
}
