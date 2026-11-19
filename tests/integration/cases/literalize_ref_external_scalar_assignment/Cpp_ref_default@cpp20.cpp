#include <cstdlib>
int main() {
auto my_data = 0;
auto shared = 1;
((my_data) != (0) ? std::abort() : static_cast<void>(0));
my_data = shared;
auto expected_data = 1;
((my_data) != (expected_data) ? std::abort() : static_cast<void>(0));
    return 0;
}
