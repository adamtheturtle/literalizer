#include <vector>
#include <utility>
struct Record0 { std::vector<int> items; };
int main() {
auto record_data = std::vector<Record0>{
    Record0{{1, 2}},
};
auto&& my_data = std::move(record_data);
    (void)my_data;
    return 0;
}
