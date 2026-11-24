#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateString("hello \"world\" -- not a comment");
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
