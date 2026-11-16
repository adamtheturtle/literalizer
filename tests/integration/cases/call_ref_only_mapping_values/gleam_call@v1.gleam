pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn consume(_value: a) -> Nil { Nil }

pub fn main() {
  let item = GInt(42)
  let _ = consume(GDict([#("field", item)]))
}
