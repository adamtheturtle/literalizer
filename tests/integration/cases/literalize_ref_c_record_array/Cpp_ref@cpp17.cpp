#include <initializer_list>
#include <string>
#include <vector>
struct Record0 { int x{}; };
#include <utility>
int main() {
auto first = std::vector{
    Record0{1},
    Record0{2},
};
auto&& my_data = std::move(first);
    (void)my_data;
    return 0;
}
