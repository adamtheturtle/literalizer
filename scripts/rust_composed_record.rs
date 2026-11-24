fn consume(mut first: Record0, second: Record0, repeated: Record0) {
    assert_eq!(first.name, "first");
    assert_eq!(first.values, [1, 2]);
    assert_eq!(second.name, "second");
    assert_eq!(second.values, [3]);
    first.values.push(99);
    assert_eq!(repeated.name, "first");
    assert_eq!(repeated.values, [1, 2]);
    print!(r#"{{"ok": true}}"#);
}
