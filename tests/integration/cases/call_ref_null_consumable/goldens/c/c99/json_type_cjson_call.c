#include <cjson/cJSON.h>
static void consume(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *literalizer_my_null_n0 = cJSON_CreateNull();
cJSON *my_null = literalizer_my_null_n0;
cJSON *literalizer_regular_null_n1 = cJSON_CreateNull();
cJSON *regular_null = literalizer_regular_null_n1;
consume(my_null);
consume(regular_null);
    return 0;
}
