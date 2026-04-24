pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}
pub fn process(_value: a, _count: b) -> Nil { panic }

pub fn main() {
  process(GInt(1), GInt(42))
  process(GInt(2), GInt(100))
}
