#include <initializer_list>
#include <string>
#include <map>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = {
    {{"name", "Alice"}, {"age", 30}},
    {{"name", "Bob"}, {"age", 25}},
};
}
