pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn process(_values: a, _count: b) -> Nil { Nil }

pub fn main() {
  let _ = process(GList([GInt(1), GDict([])]), GInt(42))
}
