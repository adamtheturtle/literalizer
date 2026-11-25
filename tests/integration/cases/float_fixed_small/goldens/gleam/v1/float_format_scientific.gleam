pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(1.0e-9),
    GFloat(-1.0e-9),
  ])
  let _ = my_data
}
