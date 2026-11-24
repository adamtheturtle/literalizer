pub type GVal {
  JFloat(Float)
  JList(List(GVal))
}

pub fn main() {
  let my_data = JList([
    JFloat(1.0e-09),
    JFloat(-1.0e-09),
  ])
  let _ = my_data
}
