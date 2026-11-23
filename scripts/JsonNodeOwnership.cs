using System;
using System.Text.Json.Nodes;

internal static class JsonNodeOwnership {
    private const string WrongSecondCopy = "initial second copy";

    internal static void Check(
        JsonNode argument, JsonNode original, int position
    ) {
        var copies = argument["copies"]!.AsArray();
        var initial = JsonNode.Parse("{\"value\":[1,2]}");
        var changed = JsonNode.Parse("{\"value\":[9,2]}");
        RequireValue(copies[0], initial, "first copy before mutation");
        RequireValue(copies[1], initial, WrongSecondCopy);
        RequireValue(original, initial, "original before mutation");

        copies[position]!["value"]![0] = 9;
        RequireValue(copies[position], changed, "mutated copy");
        RequireValue(copies[1 - position], initial, "other copy");
        RequireValue(original, initial, "original after mutation");

        // A fresh parent must accept the original without a clone.
        var reuse = new JsonArray(original);
        RequireValue(reuse[0], initial, "reattached original");
        reuse.RemoveAt(0);
    }

    internal static void ExpectWrongValue(Action run) {
        try {
            run();
        } catch (InvalidOperationException error) when (
            error.Message == "Wrong JsonNode: " + WrongSecondCopy
        ) {
            return;
        }
        throw new InvalidOperationException("Wrong value accepted");
    }

    private static void RequireValue(
        JsonNode? actual, JsonNode? expected, string location
    ) {
        if (!JsonNode.DeepEquals(actual, expected)) {
            throw new InvalidOperationException("Wrong JsonNode: " + location);
        }
    }
}
