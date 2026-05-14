pub type GVal {
  JFloat(Float)
  JList(List(GVal))
}

pub fn main() {
  let my_data = JList([
    JFloat(1.1),
    JFloat(-2.2),
    JFloat(3.3),
  ])
  let _ = my_data
}
