pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(1)]),
    GList([GInt(1180591620717411303424)]),
  ])
  let _ = my_data
}
