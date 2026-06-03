// =============================================
// Google Apps Script コード
// スプレッドシートの「拡張機能」→「Apps Script」に貼り付ける
// =============================================

function doGet(e) {
  const sheet  = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data   = sheet.getDataRange().getValues();

  const labels = ['とても暑い', 'やや暑い', 'ちょうどよい', 'やや寒い', 'とても寒い'];
  const counts = {};
  labels.forEach(l => counts[l] = 0);

  for (let i = 1; i < data.length; i++) {
    const answer = String(data[i][1]).trim();
    if (counts[answer] !== undefined) {
      counts[answer]++;
    }
  }

  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  const result = {
    total:      total,
    counts:     counts,
    updated_at: new Date().toISOString()
  };

  const callback = e && e.parameter && e.parameter.callback;
  const json     = JSON.stringify(result);
  const output   = callback ? callback + '(' + json + ')' : json;
  const mime     = callback
    ? ContentService.MimeType.JAVASCRIPT
    : ContentService.MimeType.JSON;

  return ContentService.createTextOutput(output).setMimeType(mime);
}
