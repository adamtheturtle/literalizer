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
pub fn process(_value: a) -> Nil { panic }

pub fn main() {
  process(GStr("hello"))
  process(GInt(42))
  process(GBool(True))
}
