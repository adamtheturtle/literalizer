pub type GVal {
  GList(List(GVal))
}
pub fn process() -> Nil { Nil }

pub fn main() {
  let _ = process()
  let _ = process()
}
