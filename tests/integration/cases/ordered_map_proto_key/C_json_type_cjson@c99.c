#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateObject();
cJSON *literalizer_my_data_n2 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(literalizer_my_data_n1, "x", literalizer_my_data_n2);
cJSON_AddItemToObject(literalizer_my_data_n0, "__proto__", literalizer_my_data_n1);
cJSON *literalizer_my_data_n3 = cJSON_CreateNumber((double)2);
cJSON_AddItemToObject(literalizer_my_data_n0, "ordinary", literalizer_my_data_n3);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
