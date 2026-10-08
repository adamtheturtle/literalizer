pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GList([GInt(1)])]),
    GList([GList([])]),
  ])
  let my_data = GList([
    GList([GList([GInt(1)])]),
    GList([GList([])]),
  ])
  let _ = my_data
}
