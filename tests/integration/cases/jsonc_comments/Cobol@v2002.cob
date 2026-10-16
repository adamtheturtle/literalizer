IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    *> A JSONC input case with both comment forms.
    05 F-URL PIC X(26) VALUE "https://example.org/a/*b*/".  *> detail
    *> continued
    05 F-COUNT PIC S9(18) COMP-5 VALUE 2.  *> trailing line comment
PROCEDURE DIVISION.
    STOP RUN.
