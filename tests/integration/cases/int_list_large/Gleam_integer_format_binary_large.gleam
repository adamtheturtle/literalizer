pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0b11110100001001000000),
    GInt(-1234),
    GInt(0b11111111),
    GInt(-10),
  ])
  let _ = my_data
}
