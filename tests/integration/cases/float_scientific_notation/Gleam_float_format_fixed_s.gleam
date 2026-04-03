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
  let my_data = GList([
    GFloat(0.000000),
    GFloat(1.000000),
    GFloat(1500.000000),
    GFloat(0.001000),
  ])
  let _ = my_data
}
