pub type GVal {
  GInt(Int)
  GFloat(Float)
  GSet(List(GVal))
}

pub fn main() {
  let my_data = GSet([
    GFloat(1.5),
    GInt(9007199254740993),
  ])
  let _ = my_data
}
