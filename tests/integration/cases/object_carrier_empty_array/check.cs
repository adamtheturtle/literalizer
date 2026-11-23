static void CheckValue(object?[] values) {
    if (values.Length != 0) {
        throw new System.InvalidOperationException("changed collection values");
    }
}
