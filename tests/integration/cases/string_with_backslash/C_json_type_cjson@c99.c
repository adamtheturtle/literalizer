#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateArray();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("C:\\path\\to\\file");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("back\\\\slash");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n2);
cJSON *literalizer_my_data_n3 = cJSON_CreateString("hello \\\"world\\\"");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n3);
cJSON *literalizer_my_data_n4 = cJSON_CreateString("path\\to \"# file");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n4);
cJSON *literalizer_my_data_n5 = cJSON_CreateString("trailing\\");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n5);
cJSON *literalizer_my_data_n6 = cJSON_CreateString("both \"quotes''' here");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n6);
cJSON *literalizer_my_data_n7 = cJSON_CreateString("line1\\nline2\nwith newline");
cJSON_AddItemToArray(literalizer_my_data_n0, literalizer_my_data_n7);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
