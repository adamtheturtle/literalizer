pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("1960-01-01T00:00:00+00:00"),
  ])
  let _ = my_data
}
