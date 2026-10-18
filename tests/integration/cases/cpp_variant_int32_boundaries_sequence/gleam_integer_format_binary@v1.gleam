pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-{0b10000000000000000000000000000000}),
    GInt(-{0b1111111111111111111111111111111}),
    GList([GInt(0b0)]),
  ])
  let _ = my_data
}
