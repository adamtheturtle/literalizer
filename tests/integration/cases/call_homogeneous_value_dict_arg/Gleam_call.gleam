pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  process(GDict([#("a", GInt(1)), #("b", GInt(2))]))
}
