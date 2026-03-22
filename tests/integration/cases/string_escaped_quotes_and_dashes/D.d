import std.json;
void _check() {
    auto _v = JSONValue("hello \"world\" -- not a comment");
}
