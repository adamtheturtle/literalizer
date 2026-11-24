pub type GVal {
  GStr(String)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GStr("1969-12-31T23:59:59+00:00"),
  ])
  let _ = my_data
}
