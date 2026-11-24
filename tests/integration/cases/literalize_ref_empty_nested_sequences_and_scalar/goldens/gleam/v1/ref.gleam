pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let seed = GInt(1)
  let my_data = GList([
    GList([]),
    GList([GList([])]),
    seed,
  ])
  let _ = my_data
}
