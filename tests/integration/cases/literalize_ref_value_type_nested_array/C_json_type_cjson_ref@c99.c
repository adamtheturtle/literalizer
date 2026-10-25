#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_shared_n3 = cJSON_CreateArray();
cJSON *literalizer_shared_n4 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(literalizer_shared_n3, literalizer_shared_n4);
cJSON *literalizer_shared_n5 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(literalizer_shared_n3, literalizer_shared_n5);
cJSON *shared = literalizer_shared_n3;
cJSON *literalizer_my_data_n0 = cJSON_CreateArray();
cJSON *literalizer_my_data_n1 = cJSON_Duplicate(shared, 1);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateNumber((double)42);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n2);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
