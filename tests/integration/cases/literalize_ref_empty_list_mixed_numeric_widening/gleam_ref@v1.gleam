pub type GVal {
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let empty_values = GList([])
  let integer_values = GList([
    GInt(1),
  ])
  let float_values = GList([
    GFloat(1.5),
  ])
  let my_data = GList([
    empty_values,
    integer_values,
    float_values,
  ])
  let _ = my_data
}
