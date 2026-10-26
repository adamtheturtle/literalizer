pub type GVal {
  GNull
  GList(List(GVal))
}

pub fn main() {
  let value = GNull
  let my_data = GList([
    value,
    value,
    GNull,
  ])
  let _ = my_data
}
