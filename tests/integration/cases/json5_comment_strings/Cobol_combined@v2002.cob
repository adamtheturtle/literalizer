IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    *> strings stay data
    05 FILLER PIC X(26) VALUE "https://example.org/a/*b*/".  *> URL annotation
    05 FILLER PIC X(30) VALUE "escaped quote: "" // still data".
    05 FILLER PIC X(12) VALUE "backslash: \".  *> outside the string
    05 FILLER PIC X(19) VALUE "/* not a comment */".
PROCEDURE DIVISION.
    INITIALIZE MY-DATA.
    STOP RUN.
