pub type GVal {
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-{0b101010}),
    GInt(0b0),
    GInt(0b101010),
    GFloat(-1.25),
    GFloat(0.0),
    GFloat(1.25),
  ])
  let _ = my_data
}
