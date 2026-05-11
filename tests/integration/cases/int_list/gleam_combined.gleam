pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(1),
    GInt(2),
    GInt(3),
  ])
  let my_data = GList([
    GInt(1),
    GInt(2),
    GInt(3),
  ])
  let _ = my_data
}
