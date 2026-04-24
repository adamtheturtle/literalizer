pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0b0),
    GInt(0b1),
    GInt(-1),
  ])
  let _ = my_data
}
