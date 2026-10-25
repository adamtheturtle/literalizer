import gleam/json
pub fn process(_value: json.Json) -> Nil { Nil }
pub fn emit(_argument0: json.Json, _argument1: json.Json) -> Nil { Nil }

pub fn main() {
  let _ = emit(process(json.int(1)), json.string("2024-01-15T12:00:00"))
}
