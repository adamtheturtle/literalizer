#include <initializer_list>
#include <vector>
#include <utility>
int main() {
auto shared = std::vector<int>{
    1,
    2,
};
auto&& my_data = std::move(shared);
    return 0;
}
