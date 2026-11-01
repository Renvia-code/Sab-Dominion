// Query SAIDI_WEATHER_ADJUSTED (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "saidi_weather_adjusted.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"YEAR", "STORM_COUNTY_DAYS", "SAIDI_EX_MED", "PREDICTED_FROM_WEATHER", "WEATHER_ADJUSTED_SAIDI"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"YEAR", type number}, {"STORM_COUNTY_DAYS", type number}, {"SAIDI_EX_MED", type number}, {"PREDICTED_FROM_WEATHER", type number}, {"WEATHER_ADJUSTED_SAIDI", type number}}, "en-US")
in
    Typed
