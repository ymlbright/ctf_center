$(document).ready(function(){

});

function login(){
	if ($('#user').val() != '' && $('#pwd').val() != ''){
		$.post(LoginURL, $("#loginForm").serialize(),function (data){
				if (data.status!=1){
					$('#alert').removeClass('hide');
					$('#alert').text(data.msg);
				} else
					document.location = data.jump;
			},'json');
	} else {
		$('#alert').removeClass('hide');
		$('#alert').text("Username or password is empty");
	}
	return false;
}

function register(){
	$('#alert').removeClass('hide');
	if ($('#user').val() != '' && $('#pwd').val() != ''){
		if ( $('#pwd').val() == $('#pwdcon').val() ){
			$.post(RegieterURL, $("#regForm").serialize(),function (data){
					if (data.status==-1){
						$('#alert').text("Username already exist.");
					} else if(data.status==0){
						$('#alert').text("Register failed.");
					}else
						document.location = data.jump;
				},'json');
		} else {
			$('#alert').text("Password confirm wrong.");
		}
	} else {
		$('#alert').text("Username or password is empty.");
	}
	return false;
}

function submitFlag(){
	if ( $('#flag').val() !='' ){
		$.post(SubmitURL,$("#flagForm").serialize(),function(data){
			if (data.status==1)
				location.reload();
			else if (data.status==-1){
				$('#alert').text('Flag wrong.');
				$('#alert').removeClass('hide');
			}
			else{
				$('#alert').text('Error:'+data.msg);
				$('#alert').removeClass('hide');
			}
			setInterval(function(){$('#alert').addClass('hide');},3000);
		},'json');
	}
	return false
}