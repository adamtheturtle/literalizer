IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    05 FILLER PIC X(15) VALUE "C:\path\to\file".
    05 FILLER PIC X(11) VALUE "back\\slash".
    05 FILLER PIC X(15) VALUE "hello \""world\""".
    05 FILLER PIC X(15) VALUE "path\to ""# file".
    05 FILLER PIC X(9) VALUE "trailing\".
    05 FILLER PIC X(20) VALUE "both ""quotes''' here".
    05 FILLER PIC X(25) VALUE "line1\nline2 with newline".
PROCEDURE DIVISION.
    INITIALIZE MY-DATA.
    STOP RUN.
