pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("2020-06-15T12:00:00-23:59"),
    GStr("2020-06-15T12:00:00-18:00"),
    GStr("2020-06-15T12:00:00+18:00"),
    GStr("2020-06-15T12:00:00+23:59"),
  ])
  let _ = my_data
}
