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
    GInt(1_000_000),
    GInt(-1_234),
    GInt(255),
    GInt(-10),
  ])
  let _ = my_data
}
