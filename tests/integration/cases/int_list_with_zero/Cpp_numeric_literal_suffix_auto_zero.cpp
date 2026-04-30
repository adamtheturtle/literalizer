#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<long>{
    0L,
    1L,
    -1L,
};
    (void)my_data;
    return 0;
}
