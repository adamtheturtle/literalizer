pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(1.100000),
    GFloat(-2.200000),
    GFloat(3.300000),
  ])
  let _ = my_data
}
