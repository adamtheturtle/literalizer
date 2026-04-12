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

pub fn main() {
  process(value: GStr("hello"))
  process(value: GInt(42))
  process(value: GBool(True))
  let _ = my_data
}
