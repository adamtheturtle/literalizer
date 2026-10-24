IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    05 FILLER PIC X(100) VALUE "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.".
    05 FILLER PIC S9(18) COMP-5 VALUE 1.
PROCEDURE DIVISION.
    STOP RUN.
