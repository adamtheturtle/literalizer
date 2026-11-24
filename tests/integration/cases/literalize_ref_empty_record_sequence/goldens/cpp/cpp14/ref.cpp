#include <vector>
#include <utility>
struct Record0 { int x{}; };
int main() {
auto empty_items = std::vector<Record0>{};
auto populated_items = std::vector<Record0>{
    Record0{1},
};
auto my_data = std::vector<std::vector<Record0>>{
    std::move(empty_items),
    std::move(populated_items),
};
    (void)my_data;
    return 0;
}
