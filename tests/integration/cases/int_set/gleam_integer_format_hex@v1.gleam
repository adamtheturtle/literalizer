pub type GVal {
  GInt(Int)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GInt(0x1),
    GInt(0x2),
    GInt(0x3),
  ])
  let _ = my_data
}
