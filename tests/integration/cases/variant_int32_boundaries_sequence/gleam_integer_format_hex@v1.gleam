pub type GVal {
  GInt(Int)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GInt(-{0x80000000}),
    GInt(-{0x7fffffff}),
    GList([GInt(0x0)]),
  ])
  let _ = my_data
}
