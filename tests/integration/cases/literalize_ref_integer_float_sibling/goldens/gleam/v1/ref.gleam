pub type GVal {
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let integer_value = GFloat(1.0)
  let my_data = GList([
    integer_value,
    GFloat(1.5),
  ])
  let _ = my_data
}
