pub type GVal {
  GNull
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = process(GNull)
  let _ = process(#(GInt(1), GInt(2)))
}
