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
    GFloat(0.0),
    GFloat(1.0),
    GFloat(1500.0),
    GFloat(0.001),
  ])
  let my_data = GList([
    GFloat(0.0),
    GFloat(1.0),
    GFloat(1500.0),
    GFloat(0.001),
  ])
  let _ = my_data
}
