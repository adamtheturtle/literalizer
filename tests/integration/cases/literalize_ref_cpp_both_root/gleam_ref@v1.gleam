pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let shared = GList([
    GInt(1),
    GInt(2),
  ])
  let my_data = shared
  let my_data = shared
  let _ = my_data
}
