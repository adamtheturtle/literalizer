pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0xf4240),
    GInt(-1234),
    GInt(0xff),
    GInt(-10),
  ])
  let _ = my_data
}
