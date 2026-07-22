#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
struct Record0 { std::string host; std::nullptr_t port{}; };
int main() {
auto my_data = Record0{
    "localhost",
    nullptr,  // not configured yet
};
(void)my_data;
my_data = Record0{
    "localhost",
    nullptr,  // not configured yet
};
    (void)my_data;
    return 0;
}
