Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Long() {
            999999999999999999L,
            -999999999999999999L
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Long() {
            999999999999999999L,
            -999999999999999999L
        }
    End Sub
End Module
