IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 N0 USAGE POINTER.
01 N1 USAGE POINTER.
01 N1-V PIC X(901) VALUE "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    & "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    & "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" & X"00".
01 N1-K PIC X(9) VALUE "long_str" & X"00".
01 N2 USAGE POINTER.
01 N2-V PIC X(481) VALUE "a""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""b"
    & "a""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""b" & X"00".
01 N2-K PIC X(7) VALUE "quoted" & X"00".
01 N-STATUS PIC S9(9) COMP-5.
01 MY-DATA USAGE POINTER.
PROCEDURE DIVISION.
    CALL "cJSON_CreateObject" RETURNING N0.
    CALL "cJSON_CreateString" USING BY REFERENCE N1-V RETURNING N1.
    CALL "cJSON_AddItemToObject" USING BY VALUE N0 BY REFERENCE N1-K BY VALUE N1 RETURNING N-STATUS.
    CALL "cJSON_CreateString" USING BY REFERENCE N2-V RETURNING N2.
    CALL "cJSON_AddItemToObject" USING BY VALUE N0 BY REFERENCE N2-K BY VALUE N2 RETURNING N-STATUS.
    SET MY-DATA TO N0.
    STOP RUN.
