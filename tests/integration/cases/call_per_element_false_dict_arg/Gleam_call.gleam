pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  process(GDict([#("a", GInt(1)), #("b", GStr("x"))]))
}
