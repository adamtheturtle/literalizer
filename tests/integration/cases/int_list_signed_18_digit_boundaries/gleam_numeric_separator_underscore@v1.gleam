pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(999_999_999_999_999_999),
    GInt(-999_999_999_999_999_999),
  ])
  let _ = my_data
}
