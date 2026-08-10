pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0b11110100001001000000),
    GInt(-0b10011010010),
    GInt(0b11111111),
    GInt(-0b1010),
  ])
  let _ = my_data
}
