static void CheckValue(System.Collections.Generic.HashSet<object> values) {
    if (values.Count != 2 || !values.Contains(true) || !values.Contains("")) {
        throw new System.InvalidOperationException("changed collection values");
    }
}
