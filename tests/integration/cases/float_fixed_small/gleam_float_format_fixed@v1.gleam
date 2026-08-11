pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(0.000000001),
    GFloat(-0.000000001),
  ])
  let _ = my_data
}
