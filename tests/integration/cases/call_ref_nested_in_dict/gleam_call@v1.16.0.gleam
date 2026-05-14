pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let my_var = GInt(42)
  process(GDict([#("key", my_var), #("count", GInt(42))]))
}
