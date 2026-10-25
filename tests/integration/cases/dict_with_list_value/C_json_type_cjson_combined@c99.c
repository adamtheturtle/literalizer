#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("Alice");
cJSON_AddItemToObject(literalizer_my_data_n0, "name", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateArray();
cJSON *literalizer_my_data_n3 = cJSON_CreateNumber((double)10);
cJSON_AddItemToArray(literalizer_my_data_n2, literalizer_my_data_n3);
cJSON *literalizer_my_data_n4 = cJSON_CreateNumber((double)20);
cJSON_AddItemToArray(literalizer_my_data_n2, literalizer_my_data_n4);
cJSON *literalizer_my_data_n5 = cJSON_CreateNumber((double)30);
cJSON_AddItemToArray(literalizer_my_data_n2, literalizer_my_data_n5);
cJSON_AddItemToObject(literalizer_my_data_n0, "scores", literalizer_my_data_n2);
cJSON *my_data = literalizer_my_data_n0;
(void)my_data;
cJSON *literalizer_my_data_m6 = cJSON_CreateObject();
cJSON *literalizer_my_data_m7 = cJSON_CreateString("Alice");
cJSON_AddItemToObject(literalizer_my_data_m6, "name", literalizer_my_data_m7);
cJSON *literalizer_my_data_m8 = cJSON_CreateArray();
cJSON *literalizer_my_data_m9 = cJSON_CreateNumber((double)10);
cJSON_AddItemToArray(literalizer_my_data_m8, literalizer_my_data_m9);
cJSON *literalizer_my_data_m10 = cJSON_CreateNumber((double)20);
cJSON_AddItemToArray(literalizer_my_data_m8, literalizer_my_data_m10);
cJSON *literalizer_my_data_m11 = cJSON_CreateNumber((double)30);
cJSON_AddItemToArray(literalizer_my_data_m8, literalizer_my_data_m11);
cJSON_AddItemToObject(literalizer_my_data_m6, "scores", literalizer_my_data_m8);
my_data = literalizer_my_data_m6;
    (void)my_data;
    return 0;
}
