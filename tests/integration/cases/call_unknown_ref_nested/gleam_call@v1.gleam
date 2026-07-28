pub type GVal {
  GBool(Bool)
  GList(List(GVal))
}
pub fn process(_known_value: a, _nested_missing: b) -> Nil { Nil }

pub fn main() {
  let known_value = GBool(True)
  let unknown_value = GBool(True)
  process(known_value, unknown_value)
}
