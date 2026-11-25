pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-2147483648),
    GInt(-2147483647),
    GList([GInt(0)]),
  ])
  let _ = my_data
}
