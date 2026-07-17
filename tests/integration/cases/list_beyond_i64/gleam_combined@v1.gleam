pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(9223372036854775807),
    GInt(9223372036854775808),
  ])
  let my_data = GList([
    GInt(9223372036854775807),
    GInt(9223372036854775808),
  ])
  let _ = my_data
}
