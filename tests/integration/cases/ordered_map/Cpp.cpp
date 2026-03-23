#include <initializer_list>
#include <string>
void _check() {
    [[maybe_unused]] _Any _v = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
};
}
