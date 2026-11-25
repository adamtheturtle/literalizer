#include <vector>
#include <array>
struct Record0 { std::array<int, 2> scores{}; };
int main() {
auto my_data = std::vector{
    Record0{{1, 2}},
    Record0{{3, 4}},
};
    (void)my_data;
    return 0;
}
