pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GFloat(1.500000), GFloat(2.500000)]),
    GList([GFloat(3.500000), GFloat(4.500000)]),
  ])
  let _ = my_data
}
