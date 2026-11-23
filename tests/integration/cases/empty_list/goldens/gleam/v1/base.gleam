pub type GVal {
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([])
  let _ = my_data
}
