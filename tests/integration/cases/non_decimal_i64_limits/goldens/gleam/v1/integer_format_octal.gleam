pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-{0o1000000000000000000000}),
    GInt(-{0o1}),
    GInt(0o777777777777777777777),
  ])
  let _ = my_data
}
