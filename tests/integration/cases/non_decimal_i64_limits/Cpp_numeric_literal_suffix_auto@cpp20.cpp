#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<long>{
    (-9223372036854775807LL - 1),
    -1L,
    9223372036854775807L,
};
    (void)my_data;
    return 0;
}
