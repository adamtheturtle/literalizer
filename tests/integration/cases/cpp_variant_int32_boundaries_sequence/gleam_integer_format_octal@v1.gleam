pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-{0o20000000000}),
    GInt(-{0o17777777777}),
    GList([GInt(0o0)]),
  ])
  let _ = my_data
}
