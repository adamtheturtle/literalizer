pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(0xf4240),
    GInt(-(0x4d2)),
    GInt(0xff),
    GInt(-(0xa)),
  ])
  let _ = my_data
}
