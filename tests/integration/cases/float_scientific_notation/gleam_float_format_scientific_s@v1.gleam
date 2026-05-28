pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(0.0),
    GFloat(1.0),
    GFloat(1.5e3),
    GFloat(1.0e-3),
    GFloat(1.0e16),
  ])
  let _ = my_data
}
