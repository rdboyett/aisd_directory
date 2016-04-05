$( document ).ready(function() {

	$(function() {
		
		$( "#searchBar" ).autocomplete({
			source: searchbarURL,
			minLength: 2,
			focus: function( event, ui ) {
			$( "#searchBar" ).val( ui.item.value );
			return false;
			},
		 })
		.data( "ui-autocomplete" )._renderItem = function( ul, item ) {
		    return $( "<li>" )
		      .data( "ui-autocomplete-item", item )
		      .append( "<a>" + item.label + "</a>" )
		      .appendTo( ul );
		};	
			
			
        });









  jQuery.validator.addMethod("noSpace", function(value, element) { 
     return value.indexOf(" ") < 0 && (value != "" || value != null); 
  }, "Space are not allowed");
  
  jQuery.validator.addMethod('selectcheck', function (value) {
      if (value == '' || value =='none') {
         return false;
      }else{
         return true;
      }
    }, "This field is required.");
    
    
    /***************** Advanced Search Dashboard **********************/
    
    $("#advancedSearchForm").validate({
		rules: {
			firstName: {
				require_from_group: [1, ".form-control"]
			},
			lastName: {
				require_from_group: [1, ".form-control"]
			},
			email: {
				require_from_group: [1, ".form-control"]
			},
			grade: {
				require_from_group: [1, ".form-control"]
			},
			subject: {
				require_from_group: [1, ".form-control"]
			},
			job: {
				require_from_group: [1, ".form-control"]
			},
			school: {
				require_from_group: [1, ".form-control"]
			},
			roomNumber: {
				require_from_group: [1, ".form-control"]
			},
			phone: {
				require_from_group: [1, ".form-control"]
			},
		},
	});
    
    
    $("form").each(function(){
        $(this).validate();
    });
    
    var create_group_options = { 
        //target:        '#output1',   // target element(s) to be updated with server response 
        //beforeSubmit:  load_spinner,  // pre-submit callback 
        //success:       load_class_page,  // post-submit callback 
 
        // other available options: 
        //url:       url         // override for form's 'action' attribute 
        //type:      type        // 'get' or 'post', override for form's 'method' attribute 
        dataType:  'json',        // 'xml', 'script', or 'json' (expected server response type) 
        //clearForm: true        // clear all form fields after successful submit 
        //resetForm: true        // reset the form after successful submit 
 
        // $.ajax options can be used here too, for example: 
        timeout:   3000 
    };
    
    ///--------------------Forms -----------------------------------------------
    /*
    $("#create-group-form").ajaxForm(create_group_options);
    $("#delete-group-form").ajaxForm({ 
        //success:        check_class_page,
        dataType:       'json',
        timeout:        3000,
    });
    */
    
    
    
    
    $("#addEmployeeForm").ajaxForm({ 
        success:        function(responseText){
            console.log(responseText);
            if (responseText.success) {
                //code
                $("input[name=addOrUpdate]").val("add");
                alert("Success")
            }else if (responseText.email){
                var r = confirm(responseText.email);
                if (r == true) {
                    $("input[name=addOrUpdate]").val("update");
                    $( "#addEmployeeForm" ).submit();
                }
            }else{
                alert(responseText.error);
            }
        },
        dataType:       'json',
        timeout:        3000,
    });
    
    
    
    $("#deleteThisRecord").ajaxForm({ 
        success:        function(responseText){
            console.log(responseText);
            if (responseText.success) {
                //code
                alert("Record Deleted.")
                window.location.href = "/dashboard/";
            }else{
                alert(responseText.error);
            }
        },
        dataType:       'json',
        timeout:        3000,
    });
    
    
    
    $("#uploadCSV_form").ajaxForm({
        beforeSubmit:   function(){
            $("#shade").fadeIn(600);
        },
        success:        function(responseText){
            console.log(responseText);
            $('#shade').fadeOut(600);
            if (responseText.success) {
                //code
                alert("Success")
            }else{
                alert(responseText.error);
            }
        },
        dataType:       'json',
    });
    
var opts = {
  lines: 17, // The number of lines to draw
  length: 14, // The length of each line
  width: 2, // The line thickness
  radius: 9, // The radius of the inner circle
  corners: 1, // Corner roundness (0..1)
  rotate: 0, // The rotation offset
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: '#CCC', // #rgb or #rrggbb or array of colors
  speed: 1.7, // Rounds per second
  trail: 54, // Afterglow percentage
  shadow: true, // Whether to render a shadow
  hwaccel: false, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: '50%', // Top position relative to parent
  left: '50%' // Left position relative to parent
};
var target = document.getElementById('spinner');
var spinner = new Spinner(opts).spin(target);




function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




/**************** Ajax Get User Info for display ***************************/

$(".getUserInfoClickable").click(function(){
   var userID = $(this).data('options').userID;
   console.log('userID: '+userID);
   getUserInfo(userID);
});


	function getUserInfo(userID){
	    //console.log('In getOldMessages');
            var csrftoken = getCookie('csrftoken');
	    
            // uri variable was set in the template script
            var uri = getUserInfoURI;
            var xhr = new XMLHttpRequest();
            var fd = new FormData();
            
            xhr.open("POST", uri, true);
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
		    var response = xhr.responseText;
		    console.log(response);
                    $(".userInfoDisplayClass").remove();
                    $("#userInfoDisplay").append(response);
                    $("#editButtonDirect").attr("href", "/editEmployee/"+userID);
                    $("#spinner").fadeOut();
                }
            };
            fd.append('userID', userID);
            xhr.send(fd);
        }
    



});
    
    
    
    
    
    
    
    
    
    
    
    