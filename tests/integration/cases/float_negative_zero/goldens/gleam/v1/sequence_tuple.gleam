pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = #(
    GFloat(-0.0),
    GFloat(1.5),
  )
  let _ = my_data
}
