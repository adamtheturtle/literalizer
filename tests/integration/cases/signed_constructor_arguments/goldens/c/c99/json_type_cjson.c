#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateArray();
cJSON *literalizer_my_data_n1 = cJSON_CreateNumber((double)-42);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateNumber((double)0);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateNumber((double)42);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n3);
cJSON *literalizer_my_data_n4 = cJSON_CreateNumber(-1.25);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n4);
cJSON *literalizer_my_data_n5 = cJSON_CreateNumber(0.0);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n5);
cJSON *literalizer_my_data_n6 = cJSON_CreateNumber(1.25);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n6);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
