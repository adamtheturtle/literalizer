#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(literalizer_my_data_n0, "quote\"backslash\\", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateNumber((double)2);
cJSON_AddItemToObject(literalizer_my_data_n0, "line\nbreak", literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateNumber((double)3);
cJSON_AddItemToObject(literalizer_my_data_n0, "$(literal)${text}", literalizer_my_data_n3);
cJSON *literalizer_my_data_n4 = cJSON_CreateNumber((double)4);
cJSON_AddItemToObject(literalizer_my_data_n0, "RStr prefix", literalizer_my_data_n4);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
