pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0o67405553164730777777),
    GInt(-{0o67405553164730777777}),
  ])
  let _ = my_data
}
