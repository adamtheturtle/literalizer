#include <initializer_list>
#include <string>
#include <map>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<int>>{
    //
    // document heading
    // before the first entry
    // after the key
    // before the value
    {"counts", std::vector<int>{
        // before the first item
        1,  // inline block after the comma
        // before the second item
        2,
        // trailing inside the array
    }},  // after the nested collection
    {"more", std::vector<int>{
        3,
        //
        // block heading
        // block continuation
        4,  // final inline
    }},
    // trailing inside the object
    // after the root
    // after the document
};
    (void)my_data;
    return 0;
}
