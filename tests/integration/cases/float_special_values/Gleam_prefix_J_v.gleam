pub type GVal {
  JFloat(Float)
  JList(List(GVal))
}

pub fn main() {
  let my_data = JList([
    JFloat(todo),
    JFloat(todo),
    JFloat(todo),
  ])
  let _ = my_data
}
