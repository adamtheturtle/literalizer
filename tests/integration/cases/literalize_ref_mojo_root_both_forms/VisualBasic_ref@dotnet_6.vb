Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim Whole = New Integer() {
            1,
            2
        }
        Dim my_data = Whole
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = Whole
    End Sub
End Module
