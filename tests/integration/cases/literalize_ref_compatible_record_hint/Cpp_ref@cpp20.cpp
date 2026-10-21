#include <initializer_list>
#include <string>
#include <vector>
struct Record0 { std::vector<int> items; };
#include <utility>
int main() {
auto record_data = Record0{
    .items = {
        1,
        2,
    },
};
auto&& my_data = std::move(record_data);
    (void)my_data;
    return 0;
}
