pub type GVal {
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-{0o52}),
    GInt(0o0),
    GInt(0o52),
    GFloat(-1.25),
    GFloat(0.0),
    GFloat(1.25),
  ])
  let _ = my_data
}
