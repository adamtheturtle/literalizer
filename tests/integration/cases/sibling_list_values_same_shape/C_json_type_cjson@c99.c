#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateArray();
cJSON *literalizer_my_data_n2 = cJSON_CreateNumber((double)5);
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateArray();
cJSON *literalizer_my_data_n4 = cJSON_CreateString("compile");
cJSON_AddItemToArray(literalizer_my_data_n3, literalizer_my_data_n4);
cJSON *literalizer_my_data_n5 = cJSON_CreateString("test");
cJSON_AddItemToArray(literalizer_my_data_n3, literalizer_my_data_n5);
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n3);
cJSON_AddItemToObject(literalizer_my_data_n0, "test", literalizer_my_data_n1);
cJSON *literalizer_my_data_n6 = cJSON_CreateArray();
cJSON *literalizer_my_data_n7 = cJSON_CreateNumber((double)7);
cJSON_AddItemToArray(literalizer_my_data_n6, literalizer_my_data_n7);
cJSON *literalizer_my_data_n8 = cJSON_CreateArray();
cJSON *literalizer_my_data_n9 = cJSON_CreateString("link");
cJSON_AddItemToArray(literalizer_my_data_n8, literalizer_my_data_n9);
cJSON *literalizer_my_data_n10 = cJSON_CreateString("test");
cJSON_AddItemToArray(literalizer_my_data_n8, literalizer_my_data_n10);
cJSON_AddItemToArray(literalizer_my_data_n6, literalizer_my_data_n8);
cJSON_AddItemToObject(literalizer_my_data_n0, "package", literalizer_my_data_n6);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
