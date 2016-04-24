$(document).ready(function(){
  /*$('#login-form').submit(function(event){
    event.preventDefault();
    console.log('Its happening');
    create_post();
  });

  // AJAX for posting
  function create_post() {
    console.log("create post is working!") // sanity check
    console.log($('input[name=username]').val())
  };*/

  $("a#login").on("click", function () {
    $("center#login-popup").show();
  });

  $("a#close-login-popup").on("click", function () {
    $("center#login-popup").hide();
  })

  $(document).keyup(function(esc) {
    if (esc.keyCode == 27 && $("center#login-popup").is(":visible")) $('a#close-login-popup').click();   // esc
  });

  $("a#signup").on("click", function () {
    $("center#signup-popup").show();
  });

  $("a#close-signup-popup").on("click", function () {
    $("center#signup-popup").hide();
  })

  $(document).keyup(function(esc) {
    if (esc.keyCode == 27 && $("center#signup-popup").is(":visible")) $('a#close-signup-popup').click();   // esc
  });

});

$(function() {
  $("#candidate").autocomplete({
    source: "/interview/get_candidate",
    minLength: 2,
  });
});
