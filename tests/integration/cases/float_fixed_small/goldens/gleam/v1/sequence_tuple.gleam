pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GFloat(1.0e-09),
    GFloat(-1.0e-09),
  )
  let _ = my_data
}
