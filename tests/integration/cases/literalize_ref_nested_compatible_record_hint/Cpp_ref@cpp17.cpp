#include <initializer_list>
#include <string>
#include <vector>
struct Record1 { std::vector<int> items; };
struct Record0 { Record1 outer; };
int main() {
auto record_data = Record1{
    {
        1,
        2,
    },
};
auto my_data = Record0{
    std::move(record_data),
};
    (void)my_data;
    return 0;
}
