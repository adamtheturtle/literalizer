IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    05 F-A.

            10 F-B.
        15 FILLER PIC S9(18) COMP-5 VALUE 1.
            *> Outdented from the sequence, so the inner mapping claims this.
            10 F-C PIC S9(18) COMP-5 VALUE 2.

    *> Outdented from the inner mapping too, so the root claims this.
    05 F-D PIC S9(18) COMP-5 VALUE 3.
PROCEDURE DIVISION.
    INITIALIZE MY-DATA.
    STOP RUN.
