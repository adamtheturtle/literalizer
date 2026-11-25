pub type GVal {
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-42),
    GInt(0),
    GInt(42),
    GFloat(-1.250000),
    GFloat(0.000000),
    GFloat(1.250000),
  ])
  let _ = my_data
}
