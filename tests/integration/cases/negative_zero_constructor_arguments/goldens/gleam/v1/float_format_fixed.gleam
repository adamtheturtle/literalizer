pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(-0.000000),
    GFloat(0.000000),
  ])
  let _ = my_data
}
