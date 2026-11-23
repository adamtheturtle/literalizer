static void CheckValue(System.Collections.Generic.Dictionary<string, object> values) {
    if (values.Count != 2 || values["flag"] is not true || values["text"] is not "") {
        throw new System.InvalidOperationException("changed collection values");
    }
}
