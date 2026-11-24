pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("2024-01-15T12:30:00.123456+00:00"),
    GStr("2024-06-01T08:00:00+00:00"),
  ])
  let _ = my_data
}
