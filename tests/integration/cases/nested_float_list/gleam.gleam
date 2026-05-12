pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GFloat(1.5), GFloat(2.5)]),
    GList([GFloat(3.5), GFloat(4.5)]),
  ])
  let _ = my_data
}
