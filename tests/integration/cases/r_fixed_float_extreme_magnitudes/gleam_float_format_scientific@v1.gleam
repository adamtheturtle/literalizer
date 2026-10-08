pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(5.0e-324),
    GFloat(2.2250738585072014e-308),
    GFloat(1.0e-307),
    GFloat(1.0e21),
    GFloat(-1.5e300),
    GFloat(1.7976931348623157e308),
    GFloat(-1.7976931348623157e308),
  ])
  let _ = my_data
}
