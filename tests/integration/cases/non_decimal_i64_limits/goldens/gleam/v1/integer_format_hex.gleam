pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-{0x8000000000000000}),
    GInt(-{0x1}),
    GInt(0x7fffffffffffffff),
  ])
  let _ = my_data
}
