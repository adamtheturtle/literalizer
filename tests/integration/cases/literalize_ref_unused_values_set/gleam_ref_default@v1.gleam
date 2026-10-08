pub type GVal {
  GInt(Int)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GInt(1),
    GInt(2),
  ])
  let _ = my_data
}
