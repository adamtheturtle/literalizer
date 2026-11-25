pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("1970-01-01T00:00:00.000001+00:00"),
    GStr("1969-12-31T23:59:59.500000+00:00"),
    GStr("1970-01-01T00:00:01+00:00"),
  ])
  let _ = my_data
}
