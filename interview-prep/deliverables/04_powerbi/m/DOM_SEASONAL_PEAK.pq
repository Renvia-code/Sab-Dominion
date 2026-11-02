// Query DOM_SEASONAL_PEAK (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "dom_seasonal_peak.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"YEAR", "SEASON", "PEAK_MW", "PEAK_DATE", "PEAK_HOUR_NO", "HOURS_REPORTED"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"YEAR", Int64.Type}, {"SEASON", type text}, {"PEAK_MW", type number}, {"PEAK_DATE", type datetime}, {"PEAK_HOUR_NO", Int64.Type}, {"HOURS_REPORTED", Int64.Type}}, "en-US")
in
    Typed
