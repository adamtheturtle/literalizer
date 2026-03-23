#include <initializer_list>
#include <string>
void _check() {
    [[maybe_unused]] _Any _v = {
    "apple",
    "banana",
    "cherry",
};
}
