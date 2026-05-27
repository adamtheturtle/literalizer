pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(0.0),
    GFloat(1.0),
    GFloat(1500.0),
    GFloat(0.001),
    GFloat(1.0e16),
  ])
  let my_data = GList([
    GFloat(0.0),
    GFloat(1.0),
    GFloat(1500.0),
    GFloat(0.001),
    GFloat(1.0e16),
  ])
  let _ = my_data
}
