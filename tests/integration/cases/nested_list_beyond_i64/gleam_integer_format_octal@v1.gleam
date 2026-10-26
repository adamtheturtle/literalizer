pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(0o1)]),
    GList([GInt(0o200000000000000000000000)]),
  ])
  let _ = my_data
}
