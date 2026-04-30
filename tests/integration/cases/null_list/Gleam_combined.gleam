pub type GVal {
  GNull
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GNull,
    GNull,
  ])
  let my_data = GList([
    GNull,
    GNull,
  ])
  let _ = my_data
}
