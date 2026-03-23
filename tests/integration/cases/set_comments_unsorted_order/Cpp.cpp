#include <initializer_list>
#include <string>
void _check() {
    [[maybe_unused]] _Any _v = {
    // before apple
    "apple",
    "banana",  // banana inline
    // trailing
};
}
