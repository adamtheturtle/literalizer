pub type GVal {
  GInt(Int)
  GFloat(Float)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GFloat(2.5),
    GInt(1),
  ])
  let my_data = GSet([
    GFloat(2.5),
    GInt(1),
  ])
  let _ = my_data
}
