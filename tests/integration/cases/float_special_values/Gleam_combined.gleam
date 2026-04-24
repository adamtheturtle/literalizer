pub type GVal {
  GFloat(Float)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GFloat(todo),
    GFloat(todo),
    GFloat(todo),
  ])
  let my_data = GList([
    GFloat(todo),
    GFloat(todo),
    GFloat(todo),
  ])
  let _ = my_data
}
