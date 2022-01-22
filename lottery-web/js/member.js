window.member;
$(document).ready(function(){
  $.get("http://127.0.0.1:8000/lottery/employees",function(data,status){
    localStorage.setItem('member', JSON.stringify(data.data));
  });

});
