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
PROCEDURE DIVISION.
    STOP RUN.
