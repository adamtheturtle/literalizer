pub type GVal {
  GBool(Bool)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GBool(True),
    GBool(False),
    GBool(True),
  ])
  let my_data = GList([
    GBool(True),
    GBool(False),
    GBool(True),
  ])
  let _ = my_data
}
