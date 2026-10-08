#include <initializer_list>
int main() {
auto ref_flag = true;
auto&& my_data = ref_flag;
    (void)my_data;
    return 0;
}
