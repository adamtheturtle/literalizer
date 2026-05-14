pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0x1),
    GInt(0x2),
    GInt(0x3),
  ])
  let _ = my_data
}
