#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<long>{
    1L,
    2L,
    3L,
};
    (void)my_data;
    return 0;
}
