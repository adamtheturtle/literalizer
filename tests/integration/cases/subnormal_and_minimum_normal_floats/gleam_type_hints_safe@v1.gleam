pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(5.0e-324),
    GFloat(-5.0e-324),
    GFloat(2.2250738585072014e-308),
  ])
  let _ = my_data
}
