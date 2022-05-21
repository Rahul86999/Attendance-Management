{% load static %}
<!DOCTYPE html>
<html lang="en" class="no-js">
   <!--<![endif]-->
   <head>
      <meta charset="UTF-8" />
      <!-- <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">  -->
      <title>Pre-Assessment</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="description" content="Login and Registration Form with HTML5 and CSS3" />
      <meta name="keywords" content="html5, css3, form, switch, animation, :target, pseudo-class" />
      <meta name="author" content="Codrops" />
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
      <link rel="stylesheet" type="text/css" href="{% static 'css/demo.css' %}" />
      <link rel="stylesheet" type="text/css" href="{% static 'css/style2.css' %}" />
      <link rel="stylesheet" type="text/css" href="{% static 'css/animate-custom.css' %}" />
   </head>
   <body>
      <div class="container">
         <!-- Codrops top bar -->
         <div class="codrops-top">
            <div class="clr"></div>
         </div>
         <!--/ Codrops top bar -->
         <header>
            <h1>Welcome to<span> Student</span></h1>
            <nav class="codrops-demos">					
               <a href="index2.html" class="current-demo">Pre-Assessment</a>					
            </nav>
         </header>
         <section>
            <div class="dropdown">
               <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenu2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
               Select Test Category
               </button>
               <div class="dropdown-menu" aria-labelledby="dropdownMenu2">
                  {% for i in options %}
                  <button class="dropdown-item" type="button">{{i.category_name}}</button>
                  {% endfor %}
               </div>
            </div>
            {% if options %}
            {% for option in options %}
            <div id="container_demo" >
               <!-- hidden anchor to stop jump http://www.css3create.com/Astuce-Empecher-le-scroll-avec-l-utilisation-de-target#wrap4  -->
               <a class="hiddenanchor" id="toregister"></a>
               <a class="hiddenanchor" id="tologin"></a>
               <div id="wrapper">
                  <div id="login" class="animate form">
                     <form  method="post">
                        {% if messages %}
                        <ul class="messages">
                            {% for message in messages %}
                            <div class="alert alert-success">
                                <a class="close" href="#" data-dismiss="alert">×</a>

                                {{ message }}

                            </div>
                        {% endfor %}
                        </ul>
                        {% endif %}
                        {% csrf_token %}
                        <h1>Question-1</h1>
                        <audio controls style="width:70%">
                           <source src="q1.mp3" type="audio/mp3">
                        </audio>
                       
                        <p> 
                           <label> {{option.question.question_title}} </label>
                        </p>
                        <input type="radio" name="option" value="{{option.option1}}" style="margin-top:5px;"> {{option.option1}}</br>
                        <input type="radio" name="option" value="{{option.option2}}" style="margin-top:10px;"> {{option.option2}}</br>
                        <input type="radio" name="option" value="{{option.option3}}" style="margin-top:10px;"> {{option.option3}}</br>
                        <input type="radio" name="option" value="{{option.option4}}" style="margin-top:10px;"> {{option.option4}}</br></br> 
                        <p class="change_link">								
                           <!-- <a href="#toregister" class="to_register" type="submit">Submit</a> -->
                           <button class="to_register" type="submit">Submit</button>
                           <a href="#toregister" class="to_register">Skip</a>										
                        </p>
                     </form>
                  </div>
               </div>
            </div>
            {% endfor %}
            {% endif %}
         </section>
      </div>
   </body>
   <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
   <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
   <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
</html>










class QuestionDisplay(View):
	def post(self,request):
		print("ajax")
		test = AssignTest.objects.filter(student__user=request.user,test_status='started')|AssignTest.objects.filter(elearning_stu__user=request.user,test_status='started')
		test.order_by('test_datetime')
		options_ans = request.POST.get('option')
		print("answer============",options_ans)
		option1 = "Transistor"
		if test.count()==1:
			t = test.order_by('test_datetime')[0]
			print("test[0].test_paper",test[0].test_paper)
			options = Options.objects.filter(question__test=test[0].test_paper)
			print("opionnjhfdbfhj",options)
			for opt in options:
				print("=========",opt.id)
				ans_match2 = options.filter(id=opt.id)
				print("ans_match2",ans_match2)
				for opt2 in ans_match2:
					print("opt2",opt2)
			ans_match = options.filter(answer=options_ans)
			print("ans_match",ans_match)
			for i in ans_match:
				answer_point = options.get(id=i.id)
				print("ans answer_point====",answer_point)
			incorect_value = 0.0
			corect_value = 0.0
			total = 0.0
			if ans_match:
				print("answer is correct")
				# messages.success(request, 'Answer is correct')
				corect = answer_point.ans_point
				corect_value = corect +1
				print("corect_value",corect_value)
				answer_point.ans_point = corect_value
				answer_point.save()
			else:
				ans_match = options.filter(option1=option1)
				print("ans_match  ifffffffff=",ans_match)
				for data in ans_match:
					print("eslse ",data.id)
					answer_point = options.get(id=data.id)
					print("========= answer_point====",answer_point)
					corect=answer_point.ans_point
					print("Incorrect answer, Try Again !")
					incorect_value = incorect_value - 0.25
					print("incorect_value",incorect_value)
					answer_point.ans_point = incorect_value + corect
					answer_point.save()
				# messages.warning(request, 'Incorrect answer, Try Again !')
			total = corect_value + incorect_value
			print("corect_value",corect_value,"incorect_value",incorect_value,"total=====",total)
			total2 = corect_value - incorect_value
			print("corect_value",corect_value,"incorect_value",incorect_value,"total2222==========",total2)
			data = total		
			return JsonResponse(data,safe=False)
		else:
			return JsonResponse({'status':'False'})