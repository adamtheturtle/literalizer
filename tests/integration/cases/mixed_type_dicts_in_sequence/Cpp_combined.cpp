#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    {{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}},
    {{"type", "create"}, {"pr_id", "pr_2"}},
};
my_data = {
    {{"type", "create"}, {"pr_id", "pr_1"}, {"draft", true}},
    {{"type", "create"}, {"pr_id", "pr_2"}},
};
}
