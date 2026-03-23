#include <initializer_list>
#include <string>
void _check() {
    [[maybe_unused]] _Any _v = {
    true,
    42,
    "apple",
};
}
