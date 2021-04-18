var now = new Date();
  const urlParams = new URLSearchParams(window.location.search);
  const salesMonthParam = parseInt(urlParams.get('salesMonth')) || now.getMonth() + 1;
  const salesYearParam = parseInt(urlParams.get('salesYear')) || now.getFullYear();
  const usedMonthParam = parseInt(urlParams.get('usedMonth')) || now.getMonth() + 1;
  const usedYearParam = parseInt(urlParams.get('usedYear')) || now.getFullYear();

function findsale() {
  var usedMonth = usedMonthParam
  var usedYear = usedYearParam
  const month = $('#monthsale').val()
  const year = $('#yearsale').val()
  if(month > 12) {
    alert("Month must be between 1 and 12")
    $('#monthsale').val(12)
    month = 12
  }
  if(month < 1) {
    alert("Month must be between 1 and 12")
    $('#monthsale').val(1)
    month = 1
  }
  if(year < 2021) {
    alert("Year must be bigger or equal to 2021")
    $('#yearsale').val(2021)
    year = 2021
  }
   if(year > 9999) {
    alert("Year must be smaller than 9999")
    $('#yearsale').val(2021)
    year = 2021
  }
  $('#salesMonth').val(month)
  $('#salesYear').val(year)

  $('#usedMonth').val(usedMonth)
  $('#usedYear').val(usedYear)
  $('#formDate').submit()
}
function findused() {
  var saleMonth = salesMonthParam
  var saleYear = salesYearParam
  const month = $('#monthused').val()
  const year = $('#yearused').val()
  if(month > 12) {
    alert("Month must be between 1 and 12")
    $('#monthused').val(12)
    month = 12
  }
  if(month < 1) {
    alert("Month must be between 1 and 12")
    $('#monthused').val(1)
    month = 1
  }
  if(year < 2021) {
    alert("Year must be bigger or equal to 2021")
    $('#yearused').val(2021)
    year = 2021
  }
   if(year > 9999) {
    alert("Year must be smaller than 9999")
    $('#yearused').val(2021)
    year = 2021
  }
  $('#usedMonth').val(month)
  $('#usedYear').val(year)

  $('#salesMonth').val(saleMonth)
  $('#salesYear').val(saleYear)
  $('#formDate').submit()
}

function nextsale() {
  var salesMonth = salesMonthParam
  var salesYear = salesYearParam
  var usedMonth = usedMonthParam
  var usedYear = usedYearParam
  if(salesMonth + 1 > 12) {
    $('#salesYear').val(++salesYear)
    salesMonth = 0
    $('#salesMonth').val(salesMonth)
  }

  $('#salesMonth').val(salesMonth+1)
  $('#salesYear').val(salesYear)

  $('#usedMonth').val(usedMonth)
  $('#usedYear').val(usedYear)
  $('#formDate').submit()
}

function nextused() {
  var salesMonth = salesMonthParam
  var salesYear = salesYearParam
  var usedMonth = usedMonthParam
  var usedYear = usedYearParam
  if(usedMonth + 1 > 12) {
    $('#salesYear').val(++usedYear)
    usedMonth = 0
    $('#salesMonth').val(usedMonth)
  }
  $('#salesMonth').val(salesMonth)
  $('#salesYear').val(salesYear)

  $('#usedMonth').val(usedMonth+1)
  $('#usedYear').val(usedYear)
  $('#formDate').submit()
}

function backsale() {
  var salesMonth = salesMonthParam
  var salesYear = salesYearParam
  var usedMonth = usedMonthParam
  var usedYear = usedYearParam
  if(salesMonth - 1 < 1) {
    $('#salesYear').val(--salesYear)
    salesMonth = 13
    $('#salesMonth').val(salesMonth)
  }

  $('#salesMonth').val(salesMonth-1)
  $('#salesYear').val(salesYear)

  $('#usedMonth').val(usedMonth)
  $('#usedYear').val(usedYear)
  $('#formDate').submit()
}

function backused() {
  var salesMonth = salesMonthParam
  var salesYear = salesYearParam
  var usedMonth = usedMonthParam
  var usedYear = usedYearParam
  if(usedMonth - 1 < 1) {
    $('#salesYear').val(--usedYear)
    usedMonth = 13
    $('#salesMonth').val(usedMonth)
  }
  $('#salesMonth').val(salesMonth)
  $('#salesYear').val(salesYear)

  $('#usedMonth').val(usedMonth - 1)
  $('#usedYear').val(usedYear)
  $('#formDate').submit()
}