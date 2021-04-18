$( document ).ready(function() {
    fetch('/api/roomtypes')
  .then(res => res.json())
  .then(data => {
    const {types, maxCapacity} = data;
    types.forEach((type,index) => {
      $("#type").append(`<option value=${type}>${type}</option>`);
    })
    for(let index = 0; index < maxCapacity; index++ ){
          $("#numberOfGuest").append(`<option value=${index+1}>${index+1}</option>`);
    }
  });
  $('#arriveDate').prop('min', function(){
      return new Date().toJSON().split('T')[0];
   });
   $('#departureDate').prop('min', function(){
      return new Date().toJSON().split('T')[0];
   });
  function compareDate() {
      var arriveDate = document.getElementById("arriveDate").value;
      var departureDate = document.getElementById("departureDate").value;
      if (new Date(arriveDate).getTime() > new Date(departureDate).getTime()) {
            alert("Departure date must be bigger than arrive date");
            document.getElementById("departureDate").value = null;
            return false;
       }
      return true;
  }
});

