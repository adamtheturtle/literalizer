#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<long long>{
    1,
    1'099'511'627'776,
};
    (void)my_data;
    return 0;
}
