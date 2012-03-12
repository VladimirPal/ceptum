function fn_office_showFrom(add_data,inp){
	glob_add_data = add_data;
	if (glob_add_data){ glob_add_data_frm = inp.parentNode; }
	$('.errorlist').hide();
	$.fancybox(document.getElementById('office_form').innerHTML);
	return false;
}
function fn_office_submit(_this){
	
	if (!fn_office_submit_testErrors()){ return false; }
	
	fn_office_submit_send(_this);
	
	return false;
}
function fn_office_submit_testErrors(){
	var res = true;
	fn_office_tel_keyup_valupdt();
	$('.errorlist').hide();
	var ids = new Array('id_name','id_phone');
	for (var i = 0; i < ids.length; i++){
		if ($('#fancybox-outer #'+ids[i]).val() === ''){
			res = false;
			$('#fancybox-outer #'+ids[i]).parent('td').find('ul').fadeIn(600);
		}
	}
	
	return res;
}
function fn_office_submit_send(_this){
	
	//сбор данных из формы, отправка
	$.fancybox.close();
	$.fancybox.showActivity();
	var sendData = fn_office_submit_send_getdata(_this);
	if (glob_add_data){
		sendData += fn_office_add_data();
	}
	var the_url = $('#office_form .wpsc_checkout_forms').attr('action');
	
	$.ajax({type:"POST", url:the_url, data:sendData, success: function(){
		$.fancybox(document.getElementById('office_form_result').innerHTML);
	}});
}
function fn_office_add_data(){
	var sendData = '';
	if (glob_add_data_frm === null){ return; }
	var frm_inps = glob_add_data_frm.getElementsByTagName('input');
	for (var i = 0; i < frm_inps.length; i++){
		var name = frm_inps[i].name;
		if (name !== ''){
			sendData += '&'+name+'='+encodeURIComponent(frm_inps[i].value);
		}
	}
	
	return sendData;
}
function fn_office_submit_send_getdata(_this){

	var frm = document.getElementById('fancybox-outer');
	if (frm == null){ return ''; }
	
	var sendData = '';
	
	var inps = new Array('input','textarea');

	for (var j = 0; j < inps.length; j++){
	
		var frm_inps = frm.getElementsByTagName(inps[j]);
		
		for (var i = 0; i < frm_inps.length; i++){
			var name = frm_inps[i].name;
			if (name !== '' && name.slice(0,4) !== 'tmp_'){
				sendData += ((sendData==='')?'':'&')+name+'='+encodeURIComponent(frm_inps[i].value);
			}
		}
	}
	
	return sendData;
}
function fn_office_tel_keyup(_this,n){
	var go_next = false;
	if (n == 1 && _this.value.length >= 3){ go_next = true; }
	if (n == 2 && _this.value.length >= 3){ go_next = true; }
	if (n == 3 && _this.value.length >= 2){ go_next = true; }
	if (go_next){
		n++;
		var inps = _this.parentNode.getElementsByTagName('input');
		for (var i = 0; i < inps.length; i++){
			if (inps[i].className === 'phone'+n){
				inps[i].focus();
				return;
			}
		}
	}
}
function fn_office_tel_keyup_valupdt(){
	
	var _this = null;
	var els = document.getElementById('fancybox-outer').getElementsByTagName('input');
	for (var i = 0; i < els.length; i++){
		if (els[i].className === 'phone1'){
			_this = els[i];
			break;
		}
	}
	if (_this == null){ return; }
	
	
	var inps = _this.parentNode.getElementsByTagName('input');
	var val = '+7';
	for (var i = 0; i < inps.length; i++){
		if (inps[i].className.slice(0,5) === 'phone'){
			val += '-'+inps[i].value;
		}
	}
	if (val.length < 16){ val = ''; }
	$('#fancybox-outer .hidden_phone').val(val);
}
function fn_office_tel_click(_this){
	var inps = _this.parentNode.getElementsByTagName('input');
	for (var i = 0; i < inps.length; i++){
		if (inps[i].className === 'phone1'){
			inps[i].focus();
			return;
		}
	}
}
