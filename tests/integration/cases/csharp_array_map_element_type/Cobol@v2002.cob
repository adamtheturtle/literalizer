IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    05 F-D.
    10 FILLER.
        15 F-A.
            20 FILLER.
                25 F-B.
                    30 FILLER PIC S9(18) COMP-5 VALUE 1.
                    30 FILLER.
                        35 FILLER COMP-2 VALUE 2.5.
                        35 FILLER.
                            40 FILLER PIC X(1) VALUE "x".
                            40 FILLER PIC S9(18) COMP-5 VALUE 1.
PROCEDURE DIVISION.
    STOP RUN.
