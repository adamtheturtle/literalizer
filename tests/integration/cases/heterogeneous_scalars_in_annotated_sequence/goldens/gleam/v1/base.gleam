pub type GVal {
  GNull
  GBool(Bool)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GBool(True),
    GFloat(1.5),
    GNull,
    GStr("2020-01-01"),
    GStr("2020-01-01T00:00:00+00:00"),
    GList([]),
  ])
  let _ = my_data
}
