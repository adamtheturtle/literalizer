pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GList([])]),
    GList([GList([GInt(1)])]),
  ])
  let my_data = GList([
    GList([GList([])]),
    GList([GList([GInt(1)])]),
  ])
  let _ = my_data
}
