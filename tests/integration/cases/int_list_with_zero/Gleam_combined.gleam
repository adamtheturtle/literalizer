pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0),
    GInt(1),
    GInt(-1),
  ])
  let my_data = GList([
    GInt(0),
    GInt(1),
    GInt(-1),
  ])
  let _ = my_data
}
