pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let ref_x = GInt(3)
  let my_data = GList([
    ref_x,
    GInt(1),
    GInt(2),
  ])
  let _ = my_data
}
