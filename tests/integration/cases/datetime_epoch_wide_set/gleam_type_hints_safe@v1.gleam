pub type GVal {
  GStr(String)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GStr("2099-06-15T08:30:00"),
  ])
  let _ = my_data
}
