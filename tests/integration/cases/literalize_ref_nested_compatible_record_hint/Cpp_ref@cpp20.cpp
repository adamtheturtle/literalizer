#include <utility>
#include <vector>
struct Record1 { std::vector<int> items; };
struct Record0 { Record1 outer; };
int main() {
auto record_data = Record1{
    .items = {
        1,
        2,
    },
};
auto my_data = Record0{
    .outer = std::move(record_data),
};
    (void)my_data;
    return 0;
}
