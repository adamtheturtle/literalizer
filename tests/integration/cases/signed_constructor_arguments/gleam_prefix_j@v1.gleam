pub type GVal {
  JInt(Int)
  JFloat(Float)
  JList(List(GVal))
}

pub fn main() {
  let my_data = JList([
    JInt(-42),
    JInt(0),
    JInt(42),
    JFloat(-1.25),
    JFloat(0.0),
    JFloat(1.25),
  ])
  let _ = my_data
}
