IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    05 F-LONG-STR PIC X(900) VALUE "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    & "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    & "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx".
    05 F-QUOTED PIC X(480) VALUE "a""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""b"
    & "a""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""ba""b".
    05 F-WIDE PIC X(600) VALUE "中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"
    & "中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中".
PROCEDURE DIVISION.
    STOP RUN.
