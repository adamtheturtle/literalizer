#include <vector>
struct Record0 { bool active{}; };
int main() {
auto my_data = std::vector{
    Record0{.active = true},
    Record0{.active = false},
};
    (void)my_data;
    return 0;
}
