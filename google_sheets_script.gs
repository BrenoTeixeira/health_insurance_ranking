function onOpen() {

  var ui = SpreadsheetApp.getUi()
    ui.createMenu('Model')
    .addItem('Get Prediction', 'PredictAll')
    .addToUi();
}

// Get the data and transform into JSON
function doGet() {
  var content = getSheetData();
  var contentObject = content
  Logger.log(contentObject)
  return ContentService.createTextOutput(JSON.stringify(contentObject)).setMimeType(ContentService.MimeType.JSON)
};

// get the data from the sheet
function getSheetData() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var dataSheet = ss.getSheetByName('production');
  var data = dataSheet.getDataRange().getValues();
  var lastcol = dataSheet.getRange('A1:K1').getValues()[0].length;
  var lastrow = dataSheet.getLastRow();
  var json_d = []

  for (var i = 0; i < lastrow; i++) {
    var object = Object()
    if (i == 0) {} else {
                for (var j = 0; j < lastcol; j++) {
                  object[data[0][j]] = data[i][j]
                }
    json_d.push(object);
    
    };
  };
  Logger.log(object)
  return JSON.stringify(json_d)
};

function SortbyPrediction() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('production');
  var range = sheet.getRange(2, 1, sheet.getLastRow()-1, 12);
  range.sort({column: 12, ascending: false});
  range.setNumberFormat('0.00')
};

function numberFormat() {
  SpreadsheetApp.getActive().getActiveRange().setNumberFormat("####.00");
};


function PredictAll() {
  data_json = getSheetData()
  var url = 'https://cross-sell-api.onrender.com/predictions';
  var options = {
    'method': 'POST',
    'contentType': 'application/json',
    'payload': data_json
  };
  var response = UrlFetchApp.fetch(url, options);
  var json = response.getContentText();
  sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('production')

  var object = JSON.parse(json)
  var z = 2
  sheet.getRange('L1:L1').setValue('proba_prediction')

  for (let instance of object)
  {
    sheet.getRange(z, 12).setValue(instance.proba_predictions)
    z = z + 1
  };
  SortbyPrediction()
};