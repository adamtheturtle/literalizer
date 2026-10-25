#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateArray();
cJSON *literalizer_my_data_n1 = cJSON_CreateArray();
cJSON *literalizer_my_data_n2 = cJSON_CreateString("set_task");
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("web");
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n3);
cJSON *literalizer_my_data_n4 = cJSON_CreateString("lint_web");
cJSON_AddItemToArray(literalizer_my_data_n1, literalizer_my_data_n4);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n1);
cJSON *literalizer_my_data_n5 = cJSON_CreateArray();
cJSON *literalizer_my_data_n6 = cJSON_CreateString("merge_pipelines");
cJSON_AddItemToArray(literalizer_my_data_n5, literalizer_my_data_n6);
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n5);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
