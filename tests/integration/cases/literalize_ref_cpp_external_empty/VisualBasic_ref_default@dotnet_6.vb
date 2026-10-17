Imports System.Collections.Generic
Module Check
    Function consume_widget(_arg As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim item = New Integer() {
            1,
            2
        }
        Dim my_data = New Integer() {
            1,
            2
        }
        consume_widget(my_data)
        my_data = item
        consume_widget(my_data)
    End Sub
End Module
