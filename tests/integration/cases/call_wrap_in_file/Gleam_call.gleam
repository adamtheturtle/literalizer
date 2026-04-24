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
pub fn process(_a: a, _b: b) -> Nil { panic }

pub fn main() {
  process(GInt(1), GInt(2))
  process(GInt(3), GInt(4))
}
