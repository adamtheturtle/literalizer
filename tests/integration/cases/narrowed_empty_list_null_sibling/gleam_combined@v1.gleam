pub type GVal {
  GNull
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GNull]),
    GList([]),
  ])
  let my_data = GList([
    GList([GNull]),
    GList([]),
  ])
  let _ = my_data
}
