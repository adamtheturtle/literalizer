pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}
pub fn send(_value: a) -> Nil { Nil }

pub fn main() {
  send(GDict([#("a", GInt(1)), #("b", GStr("x"))]))
}
