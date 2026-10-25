#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateArray();
cJSON *literalizer_my_data_n2 = cJSON_CreateObject();
cJSON *literalizer_my_data_n3 = cJSON_CreateArray();
cJSON *literalizer_my_data_n4 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(literalizer_my_data_n3, literalizer_my_data_n4);
cJSON_AddItemToObject(literalizer_my_data_n2, "item", literalizer_my_data_n3);
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n2);
cJSON_AddItemToObject(literalizer_my_data_n0, "a", literalizer_my_data_n1);
cJSON *literalizer_my_data_n5 = cJSON_CreateArray();
cJSON *literalizer_my_data_n6 = cJSON_CreateObject();
cJSON *literalizer_my_data_n7 = cJSON_CreateArray();
cJSON *literalizer_my_data_n8 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(literalizer_my_data_n7, literalizer_my_data_n8);
cJSON *literalizer_my_data_n9 = cJSON_CreateNumber((double)3);
cJSON_AddItemToArray(literalizer_my_data_n7, literalizer_my_data_n9);
cJSON_AddItemToObject(literalizer_my_data_n6, "item", literalizer_my_data_n7);
cJSON_AddItemToArray(literalizer_my_data_n5, literalizer_my_data_n6);
cJSON_AddItemToObject(literalizer_my_data_n0, "b", literalizer_my_data_n5);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
