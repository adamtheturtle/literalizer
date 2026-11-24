#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateArray();
cJSON *literalizer_my_data_n2 = cJSON_CreateArray();
cJSON *literalizer_my_data_n3 = cJSON_CreateString("nested first line\n  indented\n\nnested last line\n");
cJSON_AddItemToArray(literalizer_my_data_n2, literalizer_my_data_n3);
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n2);
cJSON_AddItemToObject(literalizer_my_data_n0, "outer", literalizer_my_data_n1);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
