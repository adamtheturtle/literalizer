pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let empty_values = GList([])
  let integer_values = GList([
    GInt(1),
  ])
  let my_data = GList([
    empty_values,
    integer_values,
  ])
  let _ = my_data
}
