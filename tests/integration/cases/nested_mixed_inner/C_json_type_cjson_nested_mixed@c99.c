#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateArray();
cJSON *literalizer_my_data_n1 = cJSON_CreateArray();
cJSON *literalizer_my_data_n2 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("a");
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n3);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n1);
cJSON *literalizer_my_data_n4 = cJSON_CreateArray();
cJSON *literalizer_my_data_n5 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(literalizer_my_data_n4, literalizer_my_data_n5);
cJSON *literalizer_my_data_n6 = cJSON_CreateString("b");
cJSON_AddItemToArray(literalizer_my_data_n4, literalizer_my_data_n6);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n4);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
