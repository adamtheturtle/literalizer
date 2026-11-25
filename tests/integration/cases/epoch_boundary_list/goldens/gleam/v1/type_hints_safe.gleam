pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("1901-12-13T20:45:51"),
    GStr("1901-12-13T20:45:52"),
    GStr("2038-01-19T03:14:07"),
    GStr("2038-01-19T03:14:08"),
  ])
  let _ = my_data
}
