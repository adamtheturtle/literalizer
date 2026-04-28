pub type JsonVal {
  GFloat(Float)
  GList(List(JsonVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(0.0),
    GFloat(0.0),
    GFloat(0.0),
  ])
  let _ = my_data
}
