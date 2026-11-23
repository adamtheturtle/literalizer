static void CheckValue(System.Collections.Generic.Dictionary<string, object?> values) {
    if (values.Count != 2 || values["flag"] is not true || values["nothing"] is not null) {
        throw new System.InvalidOperationException("changed collection values");
    }
}
