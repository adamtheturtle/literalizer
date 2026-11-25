import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["call": JSONValue("send"), "args": JSONValue([JSONValue(1), JSONValue("email"), JSONValue("a@gmail.com"), JSONValue(100)])]),
    JSONValue(["call": JSONValue("recv"), "args": JSONValue([JSONValue(2), JSONValue("sms"), JSONValue("b@example.com"), JSONValue(200)])]),
]);
my_data = JSONValue([
    JSONValue(["call": JSONValue("send"), "args": JSONValue([JSONValue(1), JSONValue("email"), JSONValue("a@gmail.com"), JSONValue(100)])]),
    JSONValue(["call": JSONValue("recv"), "args": JSONValue([JSONValue(2), JSONValue("sms"), JSONValue("b@example.com"), JSONValue(200)])]),
]);
}
