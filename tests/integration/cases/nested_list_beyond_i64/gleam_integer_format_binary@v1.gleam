pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GInt(0b1)]),
    GList([GInt(0b10000000000000000000000000000000000000000000000000000000000000000000000)]),
  ])
  let _ = my_data
}
