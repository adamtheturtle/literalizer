#include <initializer_list>
#include <string>
#include <map>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = {
    {{"key", "hello   world"}, {"value", 1}},
};
}
