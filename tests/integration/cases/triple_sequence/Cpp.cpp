#include <initializer_list>
#include <string>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = {
    1,
    "hello",
    true,
};
}
