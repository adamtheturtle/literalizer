use record_data::{Record0, Value};
use std::collections::HashMap;

fn assert_row(row: &Record0, name: &str, attributes: &[(&str, Value)]) {
    assert_eq!(row.name, name);
    assert_eq!(row.attributes.len(), attributes.len(), "{name}");
    for (key, expected) in attributes {
        let actual = row.attributes.get(key).expect("missing attribute");
        match (actual, expected) {
            (Value::Str(actual), Value::Str(expected)) => {
                assert_eq!(actual, expected, "{name}.{key}");
            }
            (Value::Bool(actual), Value::Bool(expected)) => {
                assert_eq!(actual, expected, "{name}.{key}");
            }
            _ => panic!("{name}.{key}: wrong value type"),
        }
    }
}

fn main() {
    let declaring_data: Vec<Record0> = include!("declaring_data.rs");
    let dependent_data: Vec<Record0> = include!("dependent_data.rs");

    assert_eq!(declaring_data.len(), 2);
    assert_eq!(dependent_data.len(), 2);
    assert_row(
        &declaring_data[0],
        "row_1",
        &[
            ("colour", Value::Str("red")),
            ("discounted", Value::Bool(true)),
        ],
    );
    assert_row(
        &declaring_data[1],
        "row_2",
        &[
            ("colour", Value::Str("blue")),
            ("size", Value::Str("large")),
        ],
    );
    assert_row(
        &dependent_data[0],
        "row_3",
        &[
            ("colour", Value::Str("green")),
            ("size", Value::Str("small")),
        ],
    );
    assert_row(
        &dependent_data[1],
        "row_4",
        &[("colour", Value::Str("white"))],
    );

    print!(r#"{{"ok": true}}"#);
}
