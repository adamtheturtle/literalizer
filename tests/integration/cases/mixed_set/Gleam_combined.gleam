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
  let my_data = GSet([
    GBool(True),
    GInt(42),
    GStr("apple"),
  ])
  let my_data = GSet([
    GBool(True),
    GInt(42),
    GStr("apple"),
  ])
  let _ = my_data
}
