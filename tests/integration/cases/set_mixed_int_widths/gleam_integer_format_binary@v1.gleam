pub type GVal {
  GInt(Int)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GInt(0b1),
    GInt(0b10000000000000000000000000000000000000000),
  ])
  let _ = my_data
}
