#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_shared_n0 = cJSON_CreateArray();
cJSON *literalizer_shared_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(literalizer_shared_n0, literalizer_shared_n1);
cJSON *literalizer_shared_n2 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(literalizer_shared_n0, literalizer_shared_n2);
cJSON *shared = literalizer_shared_n0;
cJSON * my_data = shared;
(void)my_data;
my_data = shared;
    (void)my_data;
    return 0;
}
