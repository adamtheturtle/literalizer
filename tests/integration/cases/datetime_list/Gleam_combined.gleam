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
    GStr("2024-01-15T12:30:00.123456+00:00"),
    GStr("2024-06-01T08:00:00+00:00"),
  ])
  let my_data = GList([
    GStr("2024-01-15T12:30:00.123456+00:00"),
    GStr("2024-06-01T08:00:00+00:00"),
  ])
  let _ = my_data
}
