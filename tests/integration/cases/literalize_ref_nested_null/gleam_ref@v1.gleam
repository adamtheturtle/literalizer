pub type GVal {
  GNull
  GList(List(GVal))
}

pub fn main() {
  let my_null = GNull
  let my_data = GList([
    my_null,
    GNull,
  ])
  let _ = my_data
}
