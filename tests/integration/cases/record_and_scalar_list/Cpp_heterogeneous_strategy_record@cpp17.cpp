#include <variant>
#include <vector>
struct Record0 { int a{}; };
int main() {
auto my_data = std::vector<std::variant<Record0, int>>{
    Record0{1},
    2,
};
    (void)my_data;
    return 0;
}
