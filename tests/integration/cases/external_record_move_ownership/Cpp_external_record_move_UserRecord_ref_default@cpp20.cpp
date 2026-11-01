#include "../../cpp_support/include/move_only_record.hpp"
#include <utility>
struct Record0 { UserRecord child; };
auto consume_widget(auto...) { return 0; }
int main() {
auto first = Record0{
    .child = {
        .value = 1,
    },
};
consume_widget(std::move(first));
    return 0;
}
