//https://bbbootstrap.com/snippets/multi-step-form-wizard-30467045


$(document).ready(function(){


	$('#create_own_question').hide();
	$('#bulk-ques').hide();

	
	function next_page(current){
		var current_fs, next_fs, previous_fs; //fieldsets
		var opacity;
		
		current_fs = current.parent();
		next_fs = current.parent().next();
		//console.log(current_fs,next_fs);
		//Add Class Active
		$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

		//show the next fieldset
		next_fs.show();
		//hide the current fieldset with style
		current_fs.animate({opacity: 0}, {
			step: function(now) {
			// for making fielset appear animation
				opacity = 1 - now;

				current_fs.css({
				'display': 'none',
				'position': 'relative'
				});
				next_fs.css({'opacity': opacity});
			},
			duration: 600
			});
	}
	


	$(".next").click(function(){

		var status = 0;
		var current=$(this);

		if ($(this).attr('id') == 'basic-button'){
			console.log($('#basic-form'),'dskjh');
			$.validator.messages.required = '*Required';
			$('#yearPicker').valid();
			$('#quater').valid();
			$('#package').valid();
			$('#lang').valid();
			$('#date').valid();
			$('#duration').valid();
			$('#standard').valid();

			if($('#yearPicker').valid() && $('#quater').valid()  && $('#package').valid() && $('#lang').valid() && $('#date').valid() && $('#duration').valid() && $('#standard').valid()){				
				console.log('Valid')
				console.log($('#lang').val());
				$.ajax({
					type: "POST",
					url:'/Add/basic/',
					data:{
						'year':$('#yearPicker').val(),
						'quater':$('#quater').val(),
						'package':$('#package').val(),
						'lang':$('#lang').val().join(','),
						'date': $('#date').val(),
						'duration':$('#duration').val(),
						'standard' : $('#standard').val(),
						'exam_no' : $('#exam_no').val()

					},

					dataType: 'json',
					success: function (data) {
						$('#exam_no').val(data.id);
						console.log(data);
          				next_page(current);

          			}
        
				});
			}
				
			
		}	
		if ($(this).attr('id') == 'button-q-add'){
				next_page(current);
			
		}
		
		if ($(this).attr('id') == 'category-create'){
			//console.log($('#basic-form'),'dskjh');
			//next_page(current);
			$.validator.messages.required = '*Required';
			$('.cat_name').valid();
			$('.max_mark').valid();
			$('.no_question').valid();
			
			

			if($('.cat_name').valid() && $('.max_mark').valid() &&   $('.no_question').valid()){
				console.log($('.cat_name').valid(),'ghjk');
				cat_name = '';
				no_question ='';
				max_mark = '';
				cat_id = ''
				console.log('kn');
				$('.cat_name').each(function(){
					cat_name=cat_name+','+$(this).val();
					
				})



				$('.max_mark').each(function(){
					max_mark=max_mark+','+$(this).val();
					
				})

				$('.no_question').each(function(){
					no_question=no_question+','+$(this).val();
					

				})
				$('.cat_id').each(function(){
					cat_id = cat_id+','+$(this).val();
				})
			
				$.ajax({
					type: "POST",
					url:'/Add/Category/',
					data:{
						'exam_id':$('#exam_no').val(),
						'cat_name':cat_name,
						'max_mark':max_mark,
						'no_question':no_question,
						'cat_id':cat_id
					},
					dataType: 'json',
					success: function (data) {
						ids = data.cat_id.split(',');
						var i =0;
						$('.cat_id').each(function(){
							$(this).val(ids[i]);
							i=i+1;
						})
						
						$('#cat-select').empty();
						$('.cat_name').each(function(){
							
							$('#cat-select').append('<option value="'+$(this).val()+'">'+$(this).val() +'</option>')
          				});
          				next_page(current);
          			}
				});
			}


		}	
	});

$(".previous").click(function(){

current_fs = $(this).parent();
previous_fs = $(this).parent().prev();

//Remove class active
$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

//show the previous fieldset
previous_fs.show();

//hide the current fieldset with style
current_fs.animate({opacity: 0}, {
step: function(now) {
// for making fielset appear animation
opacity = 1 - now;

current_fs.css({
'display': 'none',
'position': 'relative'
});
previous_fs.css({'opacity': opacity});
},
duration: 600
});
});

$('.radio-group .radio').click(function(){
$(this).parent().find('.radio').removeClass('selected');
$(this).addClass('selected');
});

$(".submit").click(function(){
return false;
})

$('body').on('click','#add_cat',function(){

	var cat_num = $('#cat_num').val();

	cat_num=parseInt(cat_num)+1;

	$('#cat_num').val(cat_num);
	$('#cat-section').append('<div class="row cat-item" style="border-style: solid;border-width:1px;margin-bottom: 10px;">\
	   <div class="col-lg-3 col-md-3 col-sm-6">\
	   <button class="delete-cat"><span class="glyphicon glyphicon-remove" style="color:red "></span></button>\
	    <label class="label-set"for="Question Category" class="label-set">Question Category</label>\
			<input type="text" class="cat_name" name="category_name'+cat_num+'" id ="category_name'+cat_num+'" placeholder="Category Name" required/>\
		</div>\
		<div class="col-lg-3 col-md-3  col-sm-6">\
			<label class="label-set"for="no_question" class="label-set">Question to Deliever</label>\
			<input type="number" class="no_question" name="no_question'+cat_num+'" id ="no_question'+cat_num+'" required/>\
	    	<div class="invalid-feedback">Please select Test Duration</div>\
	    </div>\
	    <div class="col-lg-3 col-md-3  col-sm-6">\
		<label class="label-set"for="exampleInputEmail1" class="label-set">Max score per question*</label>\
  	    <input type="number" class="max_mark" name="max_score'+cat_num+'" id="max_score'+cat_num+'" required/>\
  	    <input type="hidden" class="cat_id" value="1">\
  	    </div>\
	  </div>');
	})

$('body').on('click','.delete-cat',function(){
	if($('.delete-cat').length>1){	
		$(this).closest('.cat-item').remove();
		//alert($(this).closest('div').find('.cat_name').val());
		/*
		$.ajax({
					type: "POST",
					url:'/Delete/Category/',
					data:{
						'exam_id':$('#exam_no').val(),
						'cat_name':cat_name,
						'max_mark':max_mark,
						'no_question':no_question
					},
					dataType: 'json',
					success: function (data) {
						console.log(data);
          				next_page(current);
          			}
				});	
		*/
	}
});
$('body').on('change','#quest_type',function(){
	if ($('#quest_type').val()=='Passage'){
		$('#no_option').hide();
		$('label[for="no_option"]').hide();
		$("#no_option").prop('required',false);
		$(".ansoptions").prop('required',false);
		$(".op-display").empty();
		$(".ans_section").empty();
	}
	else{

		$('#no_option').show();
		$('label[for="no_option"]').show();
		$("#no_option").prop('required',true);
		$(".ansoptions").prop('required',true);
		if($('#quest_type').val()=='Single'){
			console.log('hjk');
			$('#correct_ans').attr('multiple',false)

		}

		else{
			console.log('hjkk');
			$('#correct_ans').attr('multiple',true)

		}
	}


});


$('body').on('change','#no_option',function(){
	var num = parseInt($('#no_option').val());
	$('.op-display').empty();
	for (var i=0;i<num;i++){
		$('.op-display').append('<div class="col-3">\
                                <label class="label-set">Option'+parseInt(i+1)+'</label>\
                                <input type="text" class="ansoptions" id="option'+i+1+'" required></div></div>')
	}
	if($('#quest_type').val()=='Single'){

		$('.op-display').after('<div class="row ans_section"><div class="col-6">\
			 <label class="label-set">Correct Answer</label>\
			 <select id="correct_ans" class="list-dt"></select></div></div>')

	}
	else{
		$('.op-display').after('<div class="row ans_section"><div class="col-6">\
			 <label class="label-set">Correct Answer</label>\
			 <select id="correct_ans" class="list-dt" multiple></select></div></div>')

	}
	for (var i=0;i<num;i++){
			$('#correct_ans').append('<option value="'+parseInt(i)+'">Option'+parseInt(i+1)+'</option>')

	}
	
});

$('body').on('change','#action_type',function(){
	if ($('#action_type').val()=="2"){
		$('#create_own_question').show();
	}
	else{
		$('#create_own_question').hide();
	}
	if ($('#action_type').val()=="3"){
		$('#bulk-ques').show();
	}
	else{
		$('#bulk-ques').hide();
	}
});


$('body').on('click','#save_que',function(){
	$.validator.messages.required = '*Required';
			
	$('#ques_title').valid();
	$('#no_option').valid();
	opt='';
	
	
	if ($('#quest_type').val() == 'Passage'){
		
		if( $('#ques_title').valid()){
		/* if question type is passage */
			$.ajax({

					type: "POST",
					url : '/add/question/passage/',
					dataType:'json',
					data:{
							'question':$('#ques_title').val(),
							'level':$('#level').val(),
							'quest_type':$('#quest_type').val(),
							'exam_id':$('#exam_no').val(),
							'category':$('#cat-select').val()

					
					},
					success: function (data) {
                			$("#question_table").html(data.content);

                			$('#action_type').val("1");
                			$('#create_own_question').hide();
                	}
				});

		}
	}
	else{
			$('.ansoptions').valid();
			$('#correct_ans').valid();
			

			if( $('#ques_title').valid() && $('#no_option').valid() && $('.ansoptions').valid() && $('#correct_ans').valid()){
				console.log($('#correct_ans').val());
			
				$('.ansoptions').each(function(){
					opt+=$(this).val()+',';
					
				});

				if ($('#quest_type').val()=='Single'){
					var correct =  $('#correct_ans').val()+',';
					console.log(correct)

				}
				else{
						correct =''
						var ans = $('#correct_ans').val()
						for(var i=0;i<ans.length;i++){
							correct+=ans[i]+',';
						}
						console.log(correct);
				}
				$.ajax({
						type: "POST",
						url : '/add/question/',
						dataType:'json',
						data:{
							'question':$('#ques_title').val(),
							'level':$('#level').val(),
							'quest_type':$('#quest_type').val(),
							'options' :opt,
							'answer':correct,
							'exam_id':$('#exam_no').val(),
							'category':$('#cat-select').val()

						},
						success: function (data) {
                			$("#question_table").html(data.content);

                			$('#action_type').val("1");
                			$('#create_own_question').hide();
                			
                		}
                
				})

			}
		
			
	}
			
});
$('#download').click(function(){
	$.ajax({
		
		url : '/Sample/Excel/',
		data:{
			'exam_id':$('#exam_no').val(),
		},
		xhrFields: {
                'responseType': 'blob'
            },
		success: function (data) {
			var link = document.createElement('a'),
                filename = 'file.xlsx';
                link.href = URL.createObjectURL(data);
                link.download = filename;
                link.click();


		}
	});

});

$('#excelupload').click(function(){

	
	var formData = new FormData();
	
	
	formData.append("xlsx",$('#sampleexcel')[0].files[0]); 
	formData.append("exam_no",$('#exam_no').val()); 
	
	$.ajax({
		type:"POST",
       url: '/Upload/Excel/',
       data: formData,
       processData: false,
       contentType: false,
       cache: false,
       success: function (data) {
        $("#question_table").html(data.content);
		$('#action_type').val("1");
        $('#create_own_question').hide();
       }
   });
   return false;
});

$('body').on('click','.deleteq',function(){
	var qId = $(this).attr("id");

	$.ajax({
		url:'/delete/Question/',
		data:{
			'id':qId,
			'exam_id':$('#exam_no').val()
		},
		success: function (data) {
			alert('dsfdhk')
            $("#question_table").html(data.content);
			$('#action_type').val("1");
            			
        }
    });



})

});