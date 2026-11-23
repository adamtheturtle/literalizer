static void CheckValue(Record0[] values) {
    System.Collections.Generic.Dictionary<string, object> first = values[0].Payload;
    System.Collections.Generic.Dictionary<string, object> second = values[1].Payload;
    if (first["flag"] is not true || second["text"] is not "") {
        throw new System.InvalidOperationException("changed record maps");
    }
}
