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
    GStr("2024-01-15"),
    GStr("2024-06-01"),
  ])
  let _ = my_data
}
