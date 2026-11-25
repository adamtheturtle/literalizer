IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    *> heading
    05 F-A PIC X(16) VALUE "single ' // data".
    05 F-B PIC X(16) VALUE "linecontinuation".
    05 F-C PIC X(1) VALUE "\".  *> actual comment
    05 F-D PIC X(6) VALUE "  ".  *> final comment
PROCEDURE DIVISION.
    INITIALIZE MY-DATA.
    STOP RUN.
