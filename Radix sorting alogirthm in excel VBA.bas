Attribute VB_Name = "Module1"
Sub resetbubble()

Range("J3:J55").Copy Range("B3:B55")

End Sub


Sub resetcocktail()

Range("H3:H107").Copy Range("D3:D107")

    Range("F3:F107").Select
    ActiveWindow.SmallScroll Down:=-69
    Selection.FormatConditions.AddColorScale ColorScaleType:=3
    Selection.FormatConditions(Selection.FormatConditions.Count).SetFirstPriority
    Selection.FormatConditions(1).ColorScaleCriteria(1).Type = _
        xlConditionValueLowestValue
    With Selection.FormatConditions(1).ColorScaleCriteria(1).FormatColor
        .Color = 7039480
        .TintAndShade = 0
    End With
    Selection.FormatConditions(1).ColorScaleCriteria(2).Type = _
        xlConditionValuePercentile
    Selection.FormatConditions(1).ColorScaleCriteria(2).Value = 50
    With Selection.FormatConditions(1).ColorScaleCriteria(2).FormatColor
        .Color = 8711167
        .TintAndShade = 0
    End With
    Selection.FormatConditions(1).ColorScaleCriteria(3).Type = _
        xlConditionValueHighestValue
    With Selection.FormatConditions(1).ColorScaleCriteria(3).FormatColor
        .Color = 8109667
        .TintAndShade = 0
    End With

End Sub


Sub cocktail()

counter = 1

low = 100
high = -1

Range("D3").Activate

Do
    Do
        ActiveCell.Offset(1, 0).Activate
        
        If ActiveCell.Value < low And ActiveCell.Value <> "C" And ActiveCell.Value <> "N" Then
        
            low = ActiveCell.Value
            lowloc = ActiveCell.Address
            
        End If
        
        If ActiveCell.Value > high And ActiveCell.Value <> "C" And ActiveCell.Value <> "N" Then
        
            high = ActiveCell.Value
            highloc = ActiveCell.Address
        
        End If
        
    Loop Until ActiveCell.Value = "C"
    
    ' moving the lowest figure
    Range(lowloc).Activate
    ActiveCell.Value = "N"
    Range("F2").Offset((counter), 0).Activate
    ActiveCell.Value = low
    
    'moving the highest figure
    Range(highloc).Activate
    ActiveCell.Value = "N"
    Range("F108").Offset((-counter), 0).Activate
    ActiveCell.Value = high
    
    
    'If counter Mod 7 = 0 Then Application.Wait (Now + TimeValue("0:00:1"))
    
    counter = counter + 1
    
    low = 100
    high = -1
    
    Range("D2").Activate

Loop Until counter = 54

Range("F3:F107").Cut Range("D3:D107")

End Sub

Sub reset_radix()

Range("R2:R56").Copy Range("M2:M56")

End Sub

Sub radix()

Maximum = WorksheetFunction.Max(Range("M2:M55"))

max_seeker = 1

While max_seeker - Maximum < 0 ' find the number of signficant figures

    max_seeker = max_seeker * 10
    sigfig_0 = sigfig_0 + 1

Wend

sigfig_1 = sigfig

Range("M2:M55").NumberFormat = "@"

Range("M2").Activate

icounter = 0
appendage = "0"
Range("M2").Activate

Do ' places zeroes on the front of the numbers so the algorithm can interpet it
    Do
        ActiveCell.Offset(1, 0).Activate
        Selection.NumberFormat = "@"
        
        If Len(ActiveCell.Value) < sigfig_0 And ActiveCell.Value <> "C" Then
            
            ActiveCell.Value = appendage & ActiveCell.Value
    
        End If
        
    Loop Until ActiveCell.Offset(1, 0).Value = "C"
    Range("M2").Activate
    icounter = icounter + 1
    
Loop Until icounter = sigfig_0 - 1


''' old code for adding zeroes, limited to only ranges up to 999
'Do

    'ActiveCell.Offset(1, 0).Activate
    'Selection.NumberFormat = "@"
    
    'If Mid(ActiveCell.Value, 2, 1) = "" And ActiveCell.Value <> "C" Then
           
        'ActiveCell.Value = "00" & ActiveCell.Value
            
        'ElseIf Mid(ActiveCell.Value, 3, 1) = "" And ActiveCell.Value <> "C" Then
            
            'ActiveCell.Value = "0" & ActiveCell.Value

    'End If
            
'Loop Until ActiveCell.Offset(1, 0).Value = "C"

Range("M2").Activate
sigfig_0 = 3

Do ' loop stops when all signficant figures have been selected

    Do ' loop goes through the list increasing the integer in question

        Do ' loop selects numbers possessing the required integer 0,1,2,3...
        
            ActiveCell.Offset(1, 0).Activate
            
            x = Mid(ActiveCell.Value, sigfig_0, 1)
            
            If ActiveCell.Value <> "N" Then can_skip = False 'if no cells are left to check then this skips the loop
        
            If ActiveCell.Value <> "C" And ActiveCell.Value <> "N" Then
            
                If CInt(x) = bucket Then
                
                    prevloc = ActiveCell.Address
                    newloc = Range("O3").Offset(counter, 0).Address
                    Range(prevloc).Cut Range(newloc)
                    Range(prevloc).Activate
                    ActiveCell.Value = "N"
                    counter = counter + 1
                
                End If
            
            If can_skip = True Then bucket = 9
            
            can_skip = True
            
            End If

        Loop Until ActiveCell.Value = "C" 'end of series so loop ends for integer in question and increases by 1

        Range("M2").Activate

        bucket = bucket + 1
        
        
    Loop Until bucket = 10
    
    Range("O3:O55").Cut Range("M3:M55")
    bucket = 0
    counter = 0
    sigfig_0 = sigfig_0 - 1

Loop Until sigfig_0 = 0


''' This algorithm removes the zeroes from the numbers again, but it is not necessary due to the following algorithm
'icounter = 1
'While icounter < sigfig_1
    'Range("M2").Activate
    'Do
        'ActiveCell.Offset(1, 0).Activate
        'Selection.NumberFormat = "@"
        
        'If Left(ActiveCell.Value, 1) = "0" And ActiveCell.Value <> "C" Then
               
            'ActiveCell.Value = Right(ActiveCell.Value, sigfig_1 - icounter)

        'End If
         
    'Loop Until ActiveCell.Value = "C"
   'icounter = icounter + 1
'Wend


'''resets the formatting of the numbers
Range("M2").Activate
Do
    ActiveCell.Offset(1, 0).Activate
    Selection.NumberFormat = "General"
    ActiveCell.Value = CInt(ActiveCell.Value)
    
Loop Until ActiveCell.Offset(1, 0).Value = "C"

Range("M3:M55").Select
    Selection.FormatConditions.AddColorScale ColorScaleType:=3
    Selection.FormatConditions(Selection.FormatConditions.Count).SetFirstPriority
    Selection.FormatConditions(1).ColorScaleCriteria(1).Type = _
        xlConditionValueLowestValue
    With Selection.FormatConditions(1).ColorScaleCriteria(1).FormatColor
        .Color = 7039480
        .TintAndShade = 0
    End With
    Selection.FormatConditions(1).ColorScaleCriteria(2).Type = _
        xlConditionValuePercentile
    Selection.FormatConditions(1).ColorScaleCriteria(2).Value = 50
    With Selection.FormatConditions(1).ColorScaleCriteria(2).FormatColor
        .Color = 8711167
        .TintAndShade = 0
    End With
    Selection.FormatConditions(1).ColorScaleCriteria(3).Type = _
        xlConditionValueHighestValue
    With Selection.FormatConditions(1).ColorScaleCriteria(3).FormatColor
        .Color = 8109667
        .TintAndShade = 0
    End With


End Sub


Sub bubble()

Do
    counter = 0
    Range("B3").Activate
    
    Do
        
        If ActiveCell.Value > ActiveCell.Offset(1, 0).Value Then
            
            var2 = ActiveCell.Value
            var1 = ActiveCell.Offset(1, 0).Value
            
            ActiveCell.Value = var1
            ActiveCell.Offset(1, 0).Value = var2
            counter = 1
        
        End If
        
        ActiveCell.Offset(1, 0).Activate
    
    Loop Until ActiveCell.Offset(1, 0).Value = ""

Loop Until counter = 0

End Sub
