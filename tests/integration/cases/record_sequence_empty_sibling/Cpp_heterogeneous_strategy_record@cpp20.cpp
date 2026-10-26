#include <vector>
struct Record0 { int x{}; };
int main() {
auto my_data = std::vector{
    std::vector<Record0>{},
    std::vector{Record0{.x = 1}},
};
    (void)my_data;
    return 0;
}
