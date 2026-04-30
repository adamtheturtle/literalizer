pub type GVal {
  GList(List(GVal))
}
pub fn process() -> Nil { Nil }

pub fn main() {
  process()
  process()
}
