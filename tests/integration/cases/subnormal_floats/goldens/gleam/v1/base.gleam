pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(5.0e-324),
    GFloat(-5.0e-324),
    GFloat(1.0e-310),
  ])
  let _ = my_data
}
