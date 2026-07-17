Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Integer() {
            9223372036854775807UL,
            9223372036854775808UL
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Integer() {
            9223372036854775807UL,
            9223372036854775808UL
        }
    End Sub
End Module
