pub type JsonVal {
  GFloat(Float)
  GList(List(JsonVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(1.1),
    GFloat(-2.2),
    GFloat(3.3),
  ])
  let _ = my_data
}
