#include <initializer_list>
#include <string>
void _check() {
    [[maybe_unused]] _Any _v = {
    "apple",  // inline comment
    // before banana
    "banana",
    // trailing
};
}
