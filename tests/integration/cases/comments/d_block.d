import std.json;

void _check() {
    auto _v = JSONValue([
    /* Server configuration */
    "host": JSONValue("localhost"),  /* default host */
    "port": JSONValue(8080),
    /* Enable debug mode */
    "debug": JSONValue(true),
]);
}
