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
  let my_data = GStr("2024-01-15T12:30:00+00:00")
  let my_data = GStr("2024-01-15T12:30:00+00:00")
  let _ = my_data
}
