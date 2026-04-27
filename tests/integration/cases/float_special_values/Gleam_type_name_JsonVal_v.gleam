pub type JsonVal {
  GFloat(Float)
  GList(List(JsonVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(todo),
    GFloat(todo),
    GFloat(todo),
  ])
  let _ = my_data
}
