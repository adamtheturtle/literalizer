IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    05 FILLER.

            10 F-ITEM PIC X(8) VALUE "existing".
            10 FILLER PIC X(4) VALUE "kept".
            *> This comment trails the first pair.

    05 FILLER.
    10 F-ITEM PIC X(4) VALUE "next".
    10 FILLER PIC X(9) VALUE "also kept".
    *> This comment describes the last pair.
    05 FILLER.
    10 F-ITEM PIC X(4) VALUE "last".
    10 FILLER PIC X(8) VALUE "kept too".
PROCEDURE DIVISION.
    STOP RUN.
