pub type GVal {
  JFloat(Float)
  JList(List(GVal))
}

pub fn main() {
  let my_data = JList([
    JFloat(0.0),
    JFloat(0.0),
    JFloat(0.0),
  ])
  let _ = my_data
}
