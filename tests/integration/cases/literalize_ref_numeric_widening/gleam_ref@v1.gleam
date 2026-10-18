pub type GVal {
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let floating_value = GFloat(1.5)
  let integer_value = GFloat(2.0)
  let my_data = GList([
    floating_value,
    integer_value,
  ])
  let _ = my_data
}
