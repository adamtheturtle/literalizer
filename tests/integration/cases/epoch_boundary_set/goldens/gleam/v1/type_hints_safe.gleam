pub type GVal {
  GStr(String)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GStr("1901-12-13T20:45:51"),
    GStr("1901-12-13T20:45:52"),
    GStr("2038-01-19T03:14:07"),
    GStr("2038-01-19T03:14:08"),
  ])
  let _ = my_data
}
