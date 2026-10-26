IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    05 F-BELOW.

            10 FILLER.

                    15 FILLER.

                            20 FILLER.

                                    25 FILLER.

                                            30 FILLER.

                                                    35 FILLER.

                                                            40 FILLER.

                                                                    45 FILLER PIC S9(18) COMP-5 VALUE 1.








    05 F-BOUNDARY.

            06 FILLER.

                    07 FILLER.

                            08 FILLER.

                                    09 FILLER.

                                            10 FILLER.

                                                    11 FILLER.

                                                            12 FILLER.

                                                                    13 FILLER.

                                                                            14 FILLER PIC S9(18) COMP-5 VALUE 2.









    05 F-MULTIPLE.

            06 FILLER.

                    07 FILLER.

                            08 FILLER.

                                    09 FILLER.

                                            10 FILLER.

                                                    11 FILLER.

                                                            12 FILLER.

                                                                    13 FILLER.

                                                                            14 FILLER.

                                                                                    15 FILLER.

                                                                                            16 FILLER.

                                                                                                    17 FILLER.

                                                                                                            18 FILLER.

                                                                                                                    19 FILLER.

                                                                                                                            20 FILLER.

                                                                                                                                    21 FILLER.

                                                                                                                                            22 FILLER PIC S9(18) COMP-5 VALUE 3.

















    05 F-TEXT.

            06 FILLER.

                    07 FILLER.

                            08 FILLER.

                                    09 FILLER.

                                            10 FILLER.

                                                    11 FILLER.

                                                            12 FILLER.

                                                                    13 FILLER.

                                                                            14 FILLER PIC X(5) VALUE "value".









    05 F-BOOLEAN.

            06 FILLER.

                    07 FILLER.

                            08 FILLER.

                                    09 FILLER.

                                            10 FILLER.

                                                    11 FILLER.

                                                            12 FILLER.

                                                                    13 FILLER.

                                                                            14 FILLER PIC S9(18) COMP-5 VALUE 1.









    05 F-FLOAT.

            06 FILLER.

                    07 FILLER.

                            08 FILLER.

                                    09 FILLER.

                                            10 FILLER.

                                                    11 FILLER.

                                                            12 FILLER.

                                                                    13 FILLER.

                                                                            14 FILLER COMP-2 VALUE 1.5.
PROCEDURE DIVISION.
    STOP RUN.
