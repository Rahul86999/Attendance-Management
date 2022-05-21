$(document).ready(function(){


	$('#wise').change(function(){
					
		var wise = $('#wise').val();


			if (wise == 'School Student' ){
				$('#class').prop('disabled', false);
				$('#stu_name').prop('disabled', false);
				$('#no_students').prop('disabled', false);
		

				$.ajax({
					url : '/get/School/',

					success:function(data){
						$('#name').empty();
						$('#name').append('<option>Select School</option>')
						for(var i=0;i<data.length;i++){
							$('#name').append('<option value="'+data[i].id+'">'+data[i].school_name+'</option>')
						}

					}
				})
			}
			else if (wise=='e-learning Student'){
				$.ajax({
				url:'/get/e-learning/student/',
				success:function(data){
					$('#class').prop('disabled', 'disabled');
					$('#stu_name').prop('disabled', 'disabled');
					$('#no_students').prop('disabled', 'disabled');
					
					$('#name').empty()
					$('#name').append('<option>Select Student</option>')
					
					for (var i=0;i<data.length;i++){
						$('#name').append('<option value="'+data[i].id+'">'+data[i].id+' '+data[i].student_name+'</option>')
					}
					
				}
				
			});

			}

	});

	$('#name').change(function(){
		name = $('#name').val()

		$.ajax({
			url:'/get/Class/',
			data:{
				'id':name
			},

			success:function(data){
				$('#class').empty();
				$('#class').append('<option>Select Standard</option>');
				for(var i=0;i<data.length;i++){
					$('#class').append('<option value="'+data[i].standard+'">'+data[i].standard+'</option>')
				}
				
			}
		})

	})

	$('#no_students').change(function(){
		if($('#no_students').val()=='all_student'){
			$('#stu_name').prop('disabled', 'disabled');
		
		}
		else{
			$('#stu_name').prop('disabled', false);
			name = $('#name').val();
			class_name = $('#class').val();

			$.ajax({
				url:'/get/Student/',
				data:{
					'name':name,
					'class':class_name
				},
				success:function(data){
					$('#stu_name').empty();
					$('#stu_name').attr('multiple','multiple');
					for (i=0;i<data.length;i++){
						$('#stu_name').append('<option value="'+data[i].id+'">'+data[i].id+' '+data[i].student_name +'</option>')
					}
				}
			});

		}

	});

	$('#paper_ava').click(function(){
		year =$('#year').val()
		paper_standard = $('#paper_standard').val()
		quater = $('#quater').val()
		package = $('#package').val()

		$.ajax({
			method:'POST',
			url:'/check/available/',
			data:{
				'year':year,
				'paper_standard':paper_standard,
				'quater':quater,
				'package':package
			},
			success:function(data){
				$('#p_ava').text(data.status);

			}
		})

	})




})