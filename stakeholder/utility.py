from stakeholder.models import Institution, Student, Parent,Teacher
from evaluation.models import StakeholderTag,InstitutionTag,Factor,Question
from django.db import transaction


def valided_add_student_form(first_name,last_name,student_id,father_name,mother_name,gender,dob,phone,department,student_username,student_password,email,parent_username,parent_password,parent_phone,*args, **kwargs):
    pass


def save_factors_for_institutions(instance, *args, **kwargs):

    #creating factors for institutions
    stakeholder_tag = StakeholderTag.objects.all()
    institution_tag = InstitutionTag.objects.all()

    #stakeholders
    student = stakeholder_tag[0]
    teacher = stakeholder_tag[1]
    self = stakeholder_tag[2]
    parent = stakeholder_tag[3]
    administrator = stakeholder_tag[4]

    #institutions
    primary = institution_tag[0]
    secondary = institution_tag[1]
    tertiary = institution_tag[2]

    primary_institution = "1"
    secondary_institution = "2"
    tertiary_institution = "3"
    other_institution = "4"

    if instance.institution_type == primary_institution:
        #Classroom management factor
        Classroom_Management = Factor(name="Classroom Management",description = "'Classroom management' assesses the extent to which the teacher is able to establish rules, routines, and procedures that facilitate effective teaching and learning while minimizing disruptions and behavioral problems.",institution = instance)
        Classroom_Management.save()
        Classroom_Management.institution_tag.add(tertiary,secondary,primary)
        Classroom_Management.stakeholder_tag.add(student,teacher,parent,self)

        question_8 = Question(question="Do you manage disruptive behavior or conflicts in the classroom effectively?",factor=Classroom_Management)
        question_8.save()
        question_8.stakeholder_tag.add(self)
        question_8.institution_tag.add(primary,secondary,tertiary)

        question_10 = Question(question="Does the teacher effectively handle conflicts or disciplinary issues with students?",factor=Classroom_Management)
        question_10.save()
        question_10.stakeholder_tag.add(teacher,parent)
        question_10.institution_tag.add(primary,secondary)

        question_11 = Question(question="Does the teacher keep parents informed about classroom rules and expectations, and actively involve them in improving classroom management?",factor=Classroom_Management)
        question_11.save()
        question_11.stakeholder_tag.add(parent)
        question_11.institution_tag.add(primary)

        #Communication skills factor
        Communication_Skills = Factor(name="Communication Skills",description = "'Communication skills' assesses the clarity, coherence, and appropriateness of the teacher's verbal and written communication, as well as the ability to actively listen and respond to others.",institution = instance)
        Communication_Skills.save()
        Communication_Skills.institution_tag.add(tertiary,secondary,primary)
        Communication_Skills.stakeholder_tag.add(student,teacher,parent,administrator)

        question_13 = Question(question="Does the teacher attend and perform in oraginizational seminers?",factor=Communication_Skills)
        question_13.save()
        question_13.stakeholder_tag.add(teacher,administrator)
        question_13.institution_tag.add(primary,secondary,tertiary)

        question_14 = Question(question="Does the teacher communicate with you regularly about your child's progress and academic performance?",factor=Communication_Skills)
        question_14.save()
        question_14.stakeholder_tag.add(parent)
        question_14.institution_tag.add(primary,secondary)

        question_15 = Question(question="Do you feel comfortable reaching out to the teacher with questions or concerns?",factor=Communication_Skills)
        question_15.save()
        question_15.stakeholder_tag.add(parent)
        question_15.institution_tag.add(primary,secondary)


        #Professionalism factor
        Professionalism = Factor(name="Professionalism",description = "'Professionalism' assesses the teacher's ability to maintain a high level of ethical and moral standards, follow policies and regulations, and exhibit a positive and respectful attitude towards colleagues, students, and the profession.",institution = instance)
        Professionalism.save()
        Professionalism.institution_tag.add(tertiary,secondary)
        Professionalism.stakeholder_tag.add(student)

        question_19= Question(question="Does the teacher adhere to school policies and procedures?",factor=Professionalism)
        question_19.save()
        question_19.stakeholder_tag.add(teacher,administrator)
        question_19.institution_tag.add(primary,secondary,tertiary)

        question_20= Question(question="The teacher manage time and resources effectively.",factor=Professionalism)
        question_20.save()
        question_20.stakeholder_tag.add(teacher,administrator,self)
        question_20.institution_tag.add(primary,secondary,tertiary)

        question_21= Question(question="Does the teacher demonstrate and encourage respect, honesty, and responsibility in interactions with students and colleagues?",factor=Professionalism)
        question_21.save()
        question_21.stakeholder_tag.add(administrator)
        question_21.institution_tag.add(primary,secondary,tertiary)
        
        question_22= Question(question="Does the teacher follow ethical standards and guidelines, such as maintaining confidentiality of student and school information?",factor=Professionalism)
        question_22.save()
        question_22.stakeholder_tag.add(administrator)
        question_22.institution_tag.add(primary,secondary,tertiary)

        question_23= Question(question="The teacher is always punctual and reliable, meeting deadlines and showing up prepared for all meetings and events.",factor=Professionalism)
        question_23.save()
        question_23.stakeholder_tag.add(teacher,administrator,self)
        question_23.institution_tag.add(primary,secondary,tertiary)

        question_24= Question(question="The teacher contribute to the school community outside of your classroom, such as through professional development activities or extracurricular involvement.",factor=Professionalism)
        question_24.save()
        question_24.stakeholder_tag.add(teacher,administrator,self)
        question_24.institution_tag.add(primary,secondary,tertiary)

        #Collaboration Factor
        Collaboration = Factor(name="Collaboration",description = "'Collaboration' assesses the extent to which the teacher engages in collaborative problem-solving, shares resources and knowledge, and fosters positive relationships to support student success.",institution = instance)
        Collaboration.save()
        Collaboration.institution_tag.add(primary,secondary,tertiary)
        Collaboration.stakeholder_tag.add(self,teacher,administrator)

        question_27= Question(question="Does the teacher collaborate with colleagues and administrators within their department or grade level team?",factor=Collaboration)
        question_27.save()
        question_27.stakeholder_tag.add(teacher)
        question_27.institution_tag.add(primary,secondary,tertiary)

        question_28= Question(question="Does the teacher contribute positively to team meetings and participate in decision-making processes?",factor=Collaboration)
        question_28.save()
        question_28.stakeholder_tag.add(teacher,administrator)
        question_28.institution_tag.add(primary,secondary,tertiary)

        question_29= Question(question="The teacher respond to feedback and adapt their teaching practices based on input from colleagues?",factor=Collaboration)
        question_29.save()
        question_29.stakeholder_tag.add(teacher,self)
        question_29.institution_tag.add(primary,secondary,tertiary)

        #Instructional Planning Factor
        Instructional_Planning = Factor(name="Instructional Planning",description = "'Instructional Planning' assesses the teacher's ability to plan effective and engaging lessons for their students.",institution = instance)
        Instructional_Planning.save()
        Instructional_Planning.institution_tag.add(primary,secondary,tertiary)
        Instructional_Planning.stakeholder_tag.add(self,teacher,administrator)

        question_30= Question(question="The teacher design assessments and curriculum that accurately measure student learning.",factor=Instructional_Planning)
        question_30.save()
        question_30.stakeholder_tag.add(teacher,administrator)
        question_30.institution_tag.add(primary,secondary,tertiary)

        question_31= Question(question="Do you evaluate the effectiveness of instructional plans and make revisions as needed?",factor=Instructional_Planning)
        question_31.save()
        question_31.stakeholder_tag.add(self)
        question_31.institution_tag.add(primary,secondary,tertiary)

        question_32= Question(question="Do you frequently analyze assessment data to make informed instructional decisions and adjustments?",factor=Instructional_Planning)
        question_32.save()
        question_32.stakeholder_tag.add(self)
        question_32.institution_tag.add(primary,secondary,tertiary)

        #Assessment Factor
        Assessment = Factor(name="Assessment",description = "'Assessment' assesses the teacher's proficiency in analyzing student data, identifying strengths and weaknesses, and using data to inform instructional decisions and improve student outcomes.",institution = instance)
        Assessment.save()
        Assessment.institution_tag.add(primary,secondary,tertiary)
        Assessment.stakeholder_tag.add(self,student,parent)

        question_34= Question(question="Does the teacher communicate clearly about your child's progress and areas for improvement?",factor=Assessment)
        question_34.save()
        question_34.stakeholder_tag.add(parent)
        question_34.institution_tag.add(primary)

        question_35= Question(question="Does the teacher provide timely feedback to students on their progress and work?",factor=Assessment)
        question_35.save()
        question_35.stakeholder_tag.add(parent)
        question_35.institution_tag.add(primary)

        question_38= Question(question="The teacher treting all students fairly and without bias.",factor=Assessment)
        question_38.save()
        question_38.stakeholder_tag.add(parent,self)
        question_38.institution_tag.add(primary)

        #Overall Rating
        Overall_Rating = Factor(name="Overall Rating",description = "'Overall Rating' describes the overall performance",institution = instance)
        Overall_Rating.save()
        Overall_Rating.institution_tag.add(primary,secondary,tertiary)
        Overall_Rating.stakeholder_tag.add(administrator,self,student,parent,teacher)

        question_39= Question(question="Provide an overall rating.",factor=Overall_Rating)
        question_39.save()
        question_39.stakeholder_tag.add(administrator,self,student,parent,teacher)
        question_39.institution_tag.add(primary,secondary,tertiary)











    elif instance.institution_type == secondary_institution:
        #Student Engagement Factor
        Student_Engagement = Factor(name="Student Engagement",description = "'Student engagement' assesses how effective the teacher is in creating a stimulating and interactive classroom environment that promotes active learning and student involvement.",institution = instance)
        Student_Engagement.save()
        Student_Engagement.institution_tag.add(tertiary,secondary)
        Student_Engagement.stakeholder_tag.add(student)

        question_1 = Question(question="The teacher encourage student to participate in class discussions and activities.",factor=Student_Engagement)
        question_1.save()
        question_1.stakeholder_tag.add(student)
        question_1.institution_tag.add(secondary,tertiary)

        question_2 = Question(question="The teacher make learning fun and enjoyable.",factor=Student_Engagement)
        question_2.save()
        question_2.stakeholder_tag.add(student)
        question_2.institution_tag.add(secondary,tertiary)


        #Learning outcomes Factor
        Learning_Outcomes = Factor(name="Learning Outcomes",description = "'Learning outcomes' assesses the extent to which the teacher has been successful in imparting knowledge and skills to the students and improving their academic performance.",institution = instance)
        Learning_Outcomes.save()
        Learning_Outcomes.institution_tag.add(tertiary,secondary,primary)
        Learning_Outcomes.stakeholder_tag.add(student,self)

        question_3 = Question(question="Does the teacher help you understand the material and difficult concepts effectively?",factor=Learning_Outcomes)
        question_3.save()
        question_3.stakeholder_tag.add(student)
        question_3.institution_tag.add(secondary,tertiary)

        question_4 = Question(question="Do you measure and assess student progress and achievement in your class?",factor=Learning_Outcomes)
        question_4.save()
        question_4.stakeholder_tag.add(self)
        question_4.institution_tag.add(secondary,tertiary)

        question_5 = Question(question="The teacher provide meaningful feedback to students to help them improve their learning.",factor=Learning_Outcomes)
        question_5.save()
        question_5.stakeholder_tag.add(student)
        question_5.institution_tag.add(secondary,tertiary)


        #Classroom management factor
        Classroom_Management = Factor(name="Classroom Management",description = "'Classroom management' assesses the extent to which the teacher is able to establish rules, routines, and procedures that facilitate effective teaching and learning while minimizing disruptions and behavioral problems.",institution = instance)
        Classroom_Management.save()
        Classroom_Management.institution_tag.add(tertiary,secondary,primary)
        Classroom_Management.stakeholder_tag.add(student,teacher,parent,self)


        question_6 = Question(question="Does the teacher establish and maintain a positive classroom environment?",factor=Classroom_Management)
        question_6.save()
        question_6.stakeholder_tag.add(student)
        question_6.institution_tag.add(secondary,tertiary)

        question_7 = Question(question="Does the teacher provide clear and concise directions for activities and assignments?",factor=Classroom_Management)
        question_7.save()
        question_7.stakeholder_tag.add(student)
        question_7.institution_tag.add(secondary,tertiary)

        question_8 = Question(question="Do you manage disruptive behavior or conflicts in the classroom effectively?",factor=Classroom_Management)
        question_8.save()
        question_8.stakeholder_tag.add(self)
        question_8.institution_tag.add(primary,secondary,tertiary)

        question_9 = Question(question="The teacher use a variety of instructional strategies, technologies and resources to support student learning.",factor=Classroom_Management)
        question_9.save()
        question_9.stakeholder_tag.add(student,teacher)
        question_9.institution_tag.add(secondary,tertiary)

        question_10 = Question(question="Does the teacher effectively handle conflicts or disciplinary issues with students?",factor=Classroom_Management)
        question_10.save()
        question_10.stakeholder_tag.add(teacher,parent)
        question_10.institution_tag.add(primary,secondary)

        #Communication skills factor
        Communication_Skills = Factor(name="Communication Skills",description = "'Communication skills' assesses the clarity, coherence, and appropriateness of the teacher's verbal and written communication, as well as the ability to actively listen and respond to others.",institution = instance)
        Communication_Skills.save()
        Communication_Skills.institution_tag.add(tertiary,secondary,primary)
        Communication_Skills.stakeholder_tag.add(student,teacher,parent,administrator)


        question_12 = Question(question="Does the teacher listen to and respond to students' questions and concerns?",factor=Communication_Skills)
        question_12.save()
        question_12.stakeholder_tag.add(student)
        question_12.institution_tag.add(secondary,tertiary)

        question_13 = Question(question="Does the teacher attend and perform in oraginizational seminers?",factor=Communication_Skills)
        question_13.save()
        question_13.stakeholder_tag.add(teacher,administrator)
        question_13.institution_tag.add(primary,secondary,tertiary)

        question_14 = Question(question="Does the teacher communicate with you regularly about your child's progress and academic performance?",factor=Communication_Skills)
        question_14.save()
        question_14.stakeholder_tag.add(parent)
        question_14.institution_tag.add(primary,secondary)

        question_15 = Question(question="Do you feel comfortable reaching out to the teacher with questions or concerns?",factor=Communication_Skills)
        question_15.save()
        question_15.stakeholder_tag.add(parent)
        question_15.institution_tag.add(primary,secondary)

        #Counseling & Mentoring factor
        Counseling_Mentoring = Factor(name="Counseling & Mentoring",description = "'Counseling & Mentoring' assesses the teacher's ability to provide guidance, support, and mentorship to students, particularly those who need extra assistance.",institution = instance)
        Counseling_Mentoring.save()
        Counseling_Mentoring.institution_tag.add(tertiary,secondary)
        Counseling_Mentoring.stakeholder_tag.add(student)

        question_16 = Question(question="Does the teacher provide guidance and support to students who may be struggling academically, emotionally, or socially?",factor=Counseling_Mentoring)
        question_16.save()
        question_16.stakeholder_tag.add(student)
        question_16.institution_tag.add(secondary,tertiary)

        question_17= Question(question="Does the teacher support and help you understand any concepts other than class time?",factor=Counseling_Mentoring)
        question_17.save()
        question_17.stakeholder_tag.add(student)
        question_17.institution_tag.add(secondary,tertiary)


        #Professionalism factor
        Professionalism = Factor(name="Professionalism",description = "'Professionalism' assesses the teacher's ability to maintain a high level of ethical and moral standards, follow policies and regulations, and exhibit a positive and respectful attitude towards colleagues, students, and the profession.",institution = instance)
        Professionalism.save()
        Professionalism.institution_tag.add(tertiary,secondary)
        Professionalism.stakeholder_tag.add(student)

        question_18= Question(question="The teacher demonstrate a high level of integrity and honesty in their interactions with students.",factor=Professionalism)
        question_18.save()
        question_18.stakeholder_tag.add(student)
        question_18.institution_tag.add(secondary,tertiary)

        question_19= Question(question="Does the teacher adhere to school policies and procedures?",factor=Professionalism)
        question_19.save()
        question_19.stakeholder_tag.add(teacher,administrator)
        question_19.institution_tag.add(primary,secondary,tertiary)

        question_20= Question(question="The teacher manage time and resources effectively.",factor=Professionalism)
        question_20.save()
        question_20.stakeholder_tag.add(teacher,administrator,self)
        question_20.institution_tag.add(primary,secondary,tertiary)

        question_21= Question(question="Does the teacher demonstrate and encourage respect, honesty, and responsibility in interactions with students and colleagues?",factor=Professionalism)
        question_21.save()
        question_21.stakeholder_tag.add(administrator)
        question_21.institution_tag.add(primary,secondary,tertiary)
        
        question_22= Question(question="Does the teacher follow ethical standards and guidelines, such as maintaining confidentiality of student and school information?",factor=Professionalism)
        question_22.save()
        question_22.stakeholder_tag.add(administrator)
        question_22.institution_tag.add(primary,secondary,tertiary)

        question_23= Question(question="The teacher is always punctual and reliable, meeting deadlines and showing up prepared for all meetings and events.",factor=Professionalism)
        question_23.save()
        question_23.stakeholder_tag.add(teacher,administrator,self)
        question_23.institution_tag.add(primary,secondary,tertiary)

        question_24= Question(question="The teacher contribute to the school community outside of your classroom, such as through professional development activities or extracurricular involvement.",factor=Professionalism)
        question_24.save()
        question_24.stakeholder_tag.add(teacher,administrator,self)
        question_24.institution_tag.add(primary,secondary,tertiary)

        #Collaboration Factor
        Collaboration = Factor(name="Collaboration",description = "'Collaboration' assesses the extent to which the teacher engages in collaborative problem-solving, shares resources and knowledge, and fosters positive relationships to support student success.",institution = instance)
        Collaboration.save()
        Collaboration.institution_tag.add(primary,secondary,tertiary)
        Collaboration.stakeholder_tag.add(self,teacher,administrator)

        question_27= Question(question="Does the teacher collaborate with colleagues and administrators within their department or grade level team?",factor=Collaboration)
        question_27.save()
        question_27.stakeholder_tag.add(teacher)
        question_27.institution_tag.add(primary,secondary,tertiary)

        question_28= Question(question="Does the teacher contribute positively to team meetings and participate in decision-making processes?",factor=Collaboration)
        question_28.save()
        question_28.stakeholder_tag.add(teacher,administrator)
        question_28.institution_tag.add(primary,secondary,tertiary)

        question_29= Question(question="The teacher respond to feedback and adapt their teaching practices based on input from colleagues?",factor=Collaboration)
        question_29.save()
        question_29.stakeholder_tag.add(teacher,self)
        question_29.institution_tag.add(primary,secondary,tertiary)


        #Instructional Planning Factor
        Instructional_Planning = Factor(name="Instructional Planning",description = "'Instructional Planning' assesses the teacher's ability to plan effective and engaging lessons for their students.",institution = instance)
        Instructional_Planning.save()
        Instructional_Planning.institution_tag.add(primary,secondary,tertiary)
        Instructional_Planning.stakeholder_tag.add(self,teacher,administrator)

        question_30= Question(question="The teacher design assessments and curriculum that accurately measure student learning.",factor=Instructional_Planning)
        question_30.save()
        question_30.stakeholder_tag.add(teacher,administrator)
        question_30.institution_tag.add(primary,secondary,tertiary)

        question_31= Question(question="Do you evaluate the effectiveness of instructional plans and make revisions as needed?",factor=Instructional_Planning)
        question_31.save()
        question_31.stakeholder_tag.add(self)
        question_31.institution_tag.add(primary,secondary,tertiary)

        question_32= Question(question="Do you frequently analyze assessment data to make informed instructional decisions and adjustments?",factor=Instructional_Planning)
        question_32.save()
        question_32.stakeholder_tag.add(self)
        question_32.institution_tag.add(primary,secondary,tertiary)


        #Assessment Factor
        Assessment = Factor(name="Assessment",description = "'Assessment' assesses the teacher's proficiency in analyzing student data, identifying strengths and weaknesses, and using data to inform instructional decisions and improve student outcomes.",institution = instance)
        Assessment.save()
        Assessment.institution_tag.add(primary,secondary,tertiary)
        Assessment.stakeholder_tag.add(self,student,parent)

        question_33= Question(question="The teacher involve students in the assessment process, helping them understand their own strengths and areas for improvement?",factor=Assessment)
        question_33.save()
        question_33.stakeholder_tag.add(self,student)
        question_33.institution_tag.add(secondary,tertiary)

        question_36= Question(question="Does the teacher provide timely feedback to students on their progress and work?",factor=Assessment)
        question_36.save()
        question_36.stakeholder_tag.add(student)
        question_36.institution_tag.add(secondary,tertiary)

        question_37= Question(question="The teacher treting all students fairly and without bias.",factor=Assessment)
        question_37.save()
        question_37.stakeholder_tag.add(student,self)
        question_37.institution_tag.add(secondary,tertiary)

        #Overall Rating
        Overall_Rating = Factor(name="Overall Rating",description = "'Overall Rating' describes the overall performance",institution = instance)
        Overall_Rating.save()
        Overall_Rating.institution_tag.add(primary,secondary,tertiary)
        Overall_Rating.stakeholder_tag.add(administrator,self,student,parent,teacher)

        question_39= Question(question="Provide an overall rating.",factor=Overall_Rating)
        question_39.save()
        question_39.stakeholder_tag.add(administrator,self,student,parent,teacher)
        question_39.institution_tag.add(primary,secondary,tertiary)







    


    elif instance.institution_type == tertiary_institution:
        #Student Engagement Factor
        Student_Engagement = Factor(name="Student Engagement",description = "'Student engagement' assesses how effective the teacher is in creating a stimulating and interactive classroom environment that promotes active learning and student involvement.",institution = instance)
        Student_Engagement.save()
        Student_Engagement.institution_tag.add(tertiary,secondary)
        Student_Engagement.stakeholder_tag.add(student)

        question_1 = Question(question="The teacher encourage student to participate in class discussions and activities.",factor=Student_Engagement)
        question_1.save()
        question_1.stakeholder_tag.add(student)
        question_1.institution_tag.add(secondary,tertiary)

        question_2 = Question(question="The teacher make learning fun and enjoyable.",factor=Student_Engagement)
        question_2.save()
        question_2.stakeholder_tag.add(student)
        question_2.institution_tag.add(secondary,tertiary)


        #Learning outcomes Factor
        Learning_Outcomes = Factor(name="Learning Outcomes",description = "'Learning outcomes' assesses the extent to which the teacher has been successful in imparting knowledge and skills to the students and improving their academic performance.",institution = instance)
        Learning_Outcomes.save()
        Learning_Outcomes.institution_tag.add(tertiary,secondary,primary)
        Learning_Outcomes.stakeholder_tag.add(student,self)

        question_3 = Question(question="Does the teacher help you understand the material and difficult concepts effectively?",factor=Learning_Outcomes)
        question_3.save()
        question_3.stakeholder_tag.add(student)
        question_3.institution_tag.add(secondary,tertiary)

        question_4 = Question(question="Do you measure and assess student progress and achievement in your class?",factor=Learning_Outcomes)
        question_4.save()
        question_4.stakeholder_tag.add(self)
        question_4.institution_tag.add(secondary,tertiary)

        question_5 = Question(question="The teacher provide meaningful feedback to students to help them improve their learning.",factor=Learning_Outcomes)
        question_5.save()
        question_5.stakeholder_tag.add(student)
        question_5.institution_tag.add(secondary,tertiary)


        #Classroom management factor
        Classroom_Management = Factor(name="Classroom Management",description = "'Classroom management' assesses the extent to which the teacher is able to establish rules, routines, and procedures that facilitate effective teaching and learning while minimizing disruptions and behavioral problems.",institution = instance)
        Classroom_Management.save()
        Classroom_Management.institution_tag.add(tertiary,secondary,primary)
        Classroom_Management.stakeholder_tag.add(student,teacher,parent,self)


        question_6 = Question(question="Does the teacher establish and maintain a positive classroom environment?",factor=Classroom_Management)
        question_6.save()
        question_6.stakeholder_tag.add(student)
        question_6.institution_tag.add(secondary,tertiary)

        question_7 = Question(question="Does the teacher provide clear and concise directions for activities and assignments?",factor=Classroom_Management)
        question_7.save()
        question_7.stakeholder_tag.add(student)
        question_7.institution_tag.add(secondary,tertiary)

        question_8 = Question(question="Do you manage disruptive behavior or conflicts in the classroom effectively?",factor=Classroom_Management)
        question_8.save()
        question_8.stakeholder_tag.add(self)
        question_8.institution_tag.add(primary,secondary,tertiary)

        question_9 = Question(question="The teacher use a variety of instructional strategies, technologies and resources to support student learning.",factor=Classroom_Management)
        question_9.save()
        question_9.stakeholder_tag.add(student,teacher)
        question_9.institution_tag.add(secondary,tertiary)

        #Communication skills factor
        Communication_Skills = Factor(name="Communication Skills",description = "'Communication skills' assesses the clarity, coherence, and appropriateness of the teacher's verbal and written communication, as well as the ability to actively listen and respond to others.",institution = instance)
        Communication_Skills.save()
        Communication_Skills.institution_tag.add(tertiary,secondary,primary)
        Communication_Skills.stakeholder_tag.add(student,teacher,parent,administrator)


        question_12 = Question(question="Does the teacher listen to and respond to students' questions and concerns?",factor=Communication_Skills)
        question_12.save()
        question_12.stakeholder_tag.add(student)
        question_12.institution_tag.add(secondary,tertiary)

        question_13 = Question(question="Does the teacher attend and perform in oraginizational seminers?",factor=Communication_Skills)
        question_13.save()
        question_13.stakeholder_tag.add(teacher,administrator)
        question_13.institution_tag.add(primary,secondary,tertiary)

        #Counseling & Mentoring factor
        Counseling_Mentoring = Factor(name="Counseling & Mentoring",description = "'Counseling & Mentoring' assesses the teacher's ability to provide guidance, support, and mentorship to students, particularly those who need extra assistance.",institution = instance)
        Counseling_Mentoring.save()
        Counseling_Mentoring.institution_tag.add(tertiary,secondary)
        Counseling_Mentoring.stakeholder_tag.add(student)

        question_16 = Question(question="Does the teacher provide guidance and support to students who may be struggling academically, emotionally, or socially?",factor=Counseling_Mentoring)
        question_16.save()
        question_16.stakeholder_tag.add(student)
        question_16.institution_tag.add(secondary,tertiary)

        question_17= Question(question="Does the teacher support and help you understand any concepts other than class time?",factor=Counseling_Mentoring)
        question_17.save()
        question_17.stakeholder_tag.add(student)
        question_17.institution_tag.add(secondary,tertiary)


        #Professionalism factor
        Professionalism = Factor(name="Professionalism",description = "'Professionalism' assesses the teacher's ability to maintain a high level of ethical and moral standards, follow policies and regulations, and exhibit a positive and respectful attitude towards colleagues, students, and the profession.",institution = instance)
        Professionalism.save()
        Professionalism.institution_tag.add(tertiary,secondary)
        Professionalism.stakeholder_tag.add(student)

        question_18= Question(question="The teacher demonstrate a high level of integrity and honesty in their interactions with students.",factor=Professionalism)
        question_18.save()
        question_18.stakeholder_tag.add(student)
        question_18.institution_tag.add(secondary,tertiary)

        question_19= Question(question="Does the teacher adhere to school policies and procedures?",factor=Professionalism)
        question_19.save()
        question_19.stakeholder_tag.add(teacher,administrator)
        question_19.institution_tag.add(primary,secondary,tertiary)

        question_20= Question(question="The teacher manage time and resources effectively.",factor=Professionalism)
        question_20.save()
        question_20.stakeholder_tag.add(teacher,administrator,self)
        question_20.institution_tag.add(primary,secondary,tertiary)

        question_21= Question(question="Does the teacher demonstrate and encourage respect, honesty, and responsibility in interactions with students and colleagues?",factor=Professionalism)
        question_21.save()
        question_21.stakeholder_tag.add(administrator)
        question_21.institution_tag.add(primary,secondary,tertiary)
        
        question_22= Question(question="Does the teacher follow ethical standards and guidelines, such as maintaining confidentiality of student and school information?",factor=Professionalism)
        question_22.save()
        question_22.stakeholder_tag.add(administrator)
        question_22.institution_tag.add(primary,secondary,tertiary)

        question_23= Question(question="The teacher is always punctual and reliable, meeting deadlines and showing up prepared for all meetings and events.",factor=Professionalism)
        question_23.save()
        question_23.stakeholder_tag.add(teacher,administrator,self)
        question_23.institution_tag.add(primary,secondary,tertiary)

        question_24= Question(question="The teacher contribute to the school community outside of your classroom, such as through professional development activities or extracurricular involvement.",factor=Professionalism)
        question_24.save()
        question_24.stakeholder_tag.add(teacher,administrator,self)
        question_24.institution_tag.add(primary,secondary,tertiary)


        #Research & Development Factor
        Research_Development = Factor(name="Research & Development",description = "'Research & Development' assesses the teacher's proficiency in seeking out new teaching methods, tools, and technologies, as well as engaging in research, reflection, and collaboration with colleagues to improve instructional practices and student outcomes.",institution = instance)
        Research_Development.save()
        Research_Development.institution_tag.add(tertiary)
        Research_Development.stakeholder_tag.add(student,teacher)


        question_25= Question(question="Does the teacher stay informed about trending researches and intersted about new research and developments?",factor=Research_Development)
        question_25.save()
        question_25.stakeholder_tag.add(teacher)
        question_25.institution_tag.add(tertiary)

        question_26= Question(question="Does the teacher involve students and colleagues in their research interests?",factor=Research_Development)
        question_26.save()
        question_26.stakeholder_tag.add(teacher,student)
        question_26.institution_tag.add(tertiary)


        #Collaboration Factor
        Collaboration = Factor(name="Collaboration",description = "'Collaboration' assesses the extent to which the teacher engages in collaborative problem-solving, shares resources and knowledge, and fosters positive relationships to support student success.",institution = instance)
        Collaboration.save()
        Collaboration.institution_tag.add(primary,secondary,tertiary)
        Collaboration.stakeholder_tag.add(self,teacher,administrator)

        question_27= Question(question="Does the teacher collaborate with colleagues and administrators within their department or grade level team?",factor=Collaboration)
        question_27.save()
        question_27.stakeholder_tag.add(teacher)
        question_27.institution_tag.add(primary,secondary,tertiary)

        question_28= Question(question="Does the teacher contribute positively to team meetings and participate in decision-making processes?",factor=Collaboration)
        question_28.save()
        question_28.stakeholder_tag.add(teacher,administrator)
        question_28.institution_tag.add(primary,secondary,tertiary)

        question_29= Question(question="The teacher respond to feedback and adapt their teaching practices based on input from colleagues?",factor=Collaboration)
        question_29.save()
        question_29.stakeholder_tag.add(teacher,self)
        question_29.institution_tag.add(primary,secondary,tertiary)


        #Instructional Planning Factor
        Instructional_Planning = Factor(name="Instructional Planning",description = "'Instructional Planning' assesses the teacher's ability to plan effective and engaging lessons for their students.",institution = instance)
        Instructional_Planning.save()
        Instructional_Planning.institution_tag.add(primary,secondary,tertiary)
        Instructional_Planning.stakeholder_tag.add(self,teacher,administrator)

        question_30= Question(question="The teacher design assessments and curriculum that accurately measure student learning.",factor=Instructional_Planning)
        question_30.save()
        question_30.stakeholder_tag.add(teacher,administrator)
        question_30.institution_tag.add(primary,secondary,tertiary)

        question_31= Question(question="Do you evaluate the effectiveness of instructional plans and make revisions as needed?",factor=Instructional_Planning)
        question_31.save()
        question_31.stakeholder_tag.add(self)
        question_31.institution_tag.add(primary,secondary,tertiary)

        question_32= Question(question="Do you frequently analyze assessment data to make informed instructional decisions and adjustments?",factor=Instructional_Planning)
        question_32.save()
        question_32.stakeholder_tag.add(self)
        question_32.institution_tag.add(primary,secondary,tertiary)


        #Assessment Factor
        Assessment = Factor(name="Assessment",description = "'Assessment' assesses the teacher's proficiency in analyzing student data, identifying strengths and weaknesses, and using data to inform instructional decisions and improve student outcomes.",institution = instance)
        Assessment.save()
        Assessment.institution_tag.add(primary,secondary,tertiary)
        Assessment.stakeholder_tag.add(self,student,parent)

        question_33= Question(question="The teacher involve students in the assessment process, helping them understand their own strengths and areas for improvement?",factor=Assessment)
        question_33.save()
        question_33.stakeholder_tag.add(self,student)
        question_33.institution_tag.add(secondary,tertiary)

        question_36= Question(question="Does the teacher provide timely feedback to students on their progress and work?",factor=Assessment)
        question_36.save()
        question_36.stakeholder_tag.add(student)
        question_36.institution_tag.add(secondary,tertiary)

        question_37= Question(question="The teacher treting all students fairly and without bias.",factor=Assessment)
        question_37.save()
        question_37.stakeholder_tag.add(student,self)
        question_37.institution_tag.add(secondary,tertiary)

        #Overall Rating
        Overall_Rating = Factor(name="Overall Rating",description = "'Overall Rating' describes the overall performance",institution = instance)
        Overall_Rating.save()
        Overall_Rating.institution_tag.add(primary,secondary,tertiary)
        Overall_Rating.stakeholder_tag.add(administrator,self,student,parent,teacher)

        question_39= Question(question="Provide an overall rating.",factor=Overall_Rating)
        question_39.save()
        question_39.stakeholder_tag.add(administrator,self,student,parent,teacher)
        question_39.institution_tag.add(primary,secondary,tertiary)
    

    elif instance.institution_type == other_institution:
        pass
































""""
    #Student Engagement Factor
    Student_Engagement = Factor(name="Student Engagement",description = "'Student engagement' assesses how effective the teacher is in creating a stimulating and interactive classroom environment that promotes active learning and student involvement.",institution = instance)
    Student_Engagement.save()
    Student_Engagement.institution_tag.add(tertiary,secondary)
    Student_Engagement.stakeholder_tag.add(student)

    question_1 = Question(question="The teacher encourage student to participate in class discussions and activities.",factor=Student_Engagement)
    question_1.save()
    question_1.stakeholder_tag.add(student)
    question_1.institution_tag.add(secondary,tertiary)

    question_2 = Question(question="The teacher make learning fun and enjoyable.",factor=Student_Engagement)
    question_2.save()
    question_2.stakeholder_tag.add(student)
    question_2.institution_tag.add(secondary,tertiary)


    #Learning outcomes Factor
    Learning_Outcomes = Factor(name="Learning Outcomes",description = "'Learning outcomes' assesses the extent to which the teacher has been successful in imparting knowledge and skills to the students and improving their academic performance.",institution = instance)
    Learning_Outcomes.save()
    Learning_Outcomes.institution_tag.add(tertiary,secondary,primary)
    Learning_Outcomes.stakeholder_tag.add(student,self)

    question_3 = Question(question="Does the teacher help you understand the material and difficult concepts effectively?",factor=Learning_Outcomes)
    question_3.save()
    question_3.stakeholder_tag.add(student)
    question_3.institution_tag.add(secondary,tertiary)

    question_4 = Question(question="Do you measure and assess student progress and achievement in your class?",factor=Learning_Outcomes)
    question_4.save()
    question_4.stakeholder_tag.add(self)
    question_4.institution_tag.add(secondary,tertiary)

    question_5 = Question(question="The teacher provide meaningful feedback to students to help them improve their learning.",factor=Learning_Outcomes)
    question_5.save()
    question_5.stakeholder_tag.add(student)
    question_5.institution_tag.add(secondary,tertiary)


    #Classroom management factor
    Classroom_Management = Factor(name="Classroom Management",description = "'Classroom management' assesses the extent to which the teacher is able to establish rules, routines, and procedures that facilitate effective teaching and learning while minimizing disruptions and behavioral problems.",institution = instance)
    Classroom_Management.save()
    Classroom_Management.institution_tag.add(tertiary,secondary,primary)
    Classroom_Management.stakeholder_tag.add(student,teacher,parent,self)


    question_6 = Question(question="Does the teacher establish and maintain a positive classroom environment?",factor=Classroom_Management)
    question_6.save()
    question_6.stakeholder_tag.add(student)
    question_6.institution_tag.add(secondary,tertiary)

    question_7 = Question(question="Does the teacher provide clear and concise directions for activities and assignments?",factor=Classroom_Management)
    question_7.save()
    question_7.stakeholder_tag.add(student)
    question_7.institution_tag.add(secondary,tertiary)

    question_8 = Question(question="Do you manage disruptive behavior or conflicts in the classroom effectively?",factor=Classroom_Management)
    question_8.save()
    question_8.stakeholder_tag.add(self)
    question_8.institution_tag.add(primary,secondary,tertiary)

    question_9 = Question(question="The teacher use a variety of instructional strategies, technologies and resources to support student learning.",factor=Classroom_Management)
    question_9.save()
    question_9.stakeholder_tag.add(student,teacher)
    question_9.institution_tag.add(secondary,tertiary)

    question_10 = Question(question="Does the teacher effectively handle conflicts or disciplinary issues with students?",factor=Classroom_Management)
    question_10.save()
    question_10.stakeholder_tag.add(teacher,parent)
    question_10.institution_tag.add(primary,secondary)

    question_11 = Question(question="Does the teacher keep parents informed about classroom rules and expectations, and actively involve them in improving classroom management?",factor=Classroom_Management)
    question_11.save()
    question_11.stakeholder_tag.add(parent)
    question_11.institution_tag.add(primary)


    #Communication skills factor
    Communication_Skills = Factor(name="Communication Skills",description = "'Communication skills' assesses the clarity, coherence, and appropriateness of the teacher's verbal and written communication, as well as the ability to actively listen and respond to others.",institution = instance)
    Communication_Skills.save()
    Communication_Skills.institution_tag.add(tertiary,secondary,primary)
    Communication_Skills.stakeholder_tag.add(student,teacher,parent,administrator)


    question_12 = Question(question="Does the teacher listen to and respond to students' questions and concerns?",factor=Communication_Skills)
    question_12.save()
    question_12.stakeholder_tag.add(student)
    question_12.institution_tag.add(secondary,tertiary)

    question_13 = Question(question="Does the teacher attend and perform in oraginizational seminers?",factor=Communication_Skills)
    question_13.save()
    question_13.stakeholder_tag.add(teacher,administrator)
    question_13.institution_tag.add(primary,secondary,tertiary)

    question_14 = Question(question="Does the teacher communicate with you regularly about your child's progress and academic performance?",factor=Communication_Skills)
    question_14.save()
    question_14.stakeholder_tag.add(parent)
    question_14.institution_tag.add(primary,secondary)

    question_15 = Question(question="Do you feel comfortable reaching out to the teacher with questions or concerns?",factor=Communication_Skills)
    question_15.save()
    question_15.stakeholder_tag.add(parent)
    question_15.institution_tag.add(primary,secondary)



    #Counseling & Mentoring factor
    Counseling_Mentoring = Factor(name="Counseling & Mentoring",description = "'Counseling & Mentoring' assesses the teacher's ability to provide guidance, support, and mentorship to students, particularly those who need extra assistance.",institution = instance)
    Counseling_Mentoring.save()
    Counseling_Mentoring.institution_tag.add(tertiary,secondary)
    Counseling_Mentoring.stakeholder_tag.add(student)

    question_16 = Question(question="Does the teacher provide guidance and support to students who may be struggling academically, emotionally, or socially?",factor=Counseling_Mentoring)
    question_16.save()
    question_16.stakeholder_tag.add(student)
    question_16.institution_tag.add(secondary,tertiary)

    question_17= Question(question="Does the teacher support and help you understand any concepts other than class time?",factor=Counseling_Mentoring)
    question_17.save()
    question_17.stakeholder_tag.add(student)
    question_17.institution_tag.add(secondary,tertiary)


    #Professionalism factor
    Professionalism = Factor(name="Professionalism",description = "'Professionalism' assesses the teacher's ability to maintain a high level of ethical and moral standards, follow policies and regulations, and exhibit a positive and respectful attitude towards colleagues, students, and the profession.",institution = instance)
    Professionalism.save()
    Professionalism.institution_tag.add(tertiary,secondary)
    Professionalism.stakeholder_tag.add(student)

    question_18= Question(question="Does the teacher support and help you understand any concepts other than class time?",factor=Professionalism)
    question_18.save()
    question_18.stakeholder_tag.add(student)
    question_18.institution_tag.add(secondary,tertiary)

    question_19= Question(question="Does the teacher adhere to school policies and procedures?",factor=Professionalism)
    question_19.save()
    question_19.stakeholder_tag.add(teacher,administrator)
    question_19.institution_tag.add(primary,secondary,tertiary)

    question_20= Question(question="The teacher manage time and resources effectively.",factor=Professionalism)
    question_20.save()
    question_20.stakeholder_tag.add(teacher,administrator,self)
    question_20.institution_tag.add(primary,secondary,tertiary)

    question_21= Question(question="Does the teacher demonstrate and encourage respect, honesty, and responsibility in interactions with students and colleagues?",factor=Professionalism)
    question_21.save()
    question_21.stakeholder_tag.add(administrator)
    question_21.institution_tag.add(primary,secondary,tertiary)
    
    question_22= Question(question="Does the teacher follow ethical standards and guidelines, such as maintaining confidentiality of student and school information?",factor=Professionalism)
    question_22.save()
    question_22.stakeholder_tag.add(administrator)
    question_22.institution_tag.add(primary,secondary,tertiary)

    question_23= Question(question="The teacher is always punctual and reliable, meeting deadlines and showing up prepared for all meetings and events.",factor=Professionalism)
    question_23.save()
    question_23.stakeholder_tag.add(teacher,administrator,self)
    question_23.institution_tag.add(primary,secondary,tertiary)

    question_24= Question(question="The teacher contribute to the school community outside of your classroom, such as through professional development activities or extracurricular involvement.",factor=Professionalism)
    question_24.save()
    question_24.stakeholder_tag.add(teacher,administrator,self)
    question_24.institution_tag.add(primary,secondary,tertiary)


    #Research & Development Factor
    Research_Development = Factor(name="Research & Development",description = "'Research & Development' assesses the teacher's proficiency in seeking out new teaching methods, tools, and technologies, as well as engaging in research, reflection, and collaboration with colleagues to improve instructional practices and student outcomes.",institution = instance)
    Research_Development.save()
    Research_Development.institution_tag.add(tertiary)
    Research_Development.stakeholder_tag.add(student,teacher)


    question_25= Question(question="Does the teacher stay informed about trending researches and intersted about new research and developments?",factor=Research_Development)
    question_25.save()
    question_25.stakeholder_tag.add(teacher)
    question_25.institution_tag.add(tertiary)

    question_26= Question(question="Does the teacher involve students and colleagues in their research interests?",factor=Research_Development)
    question_26.save()
    question_26.stakeholder_tag.add(teacher,student)
    question_26.institution_tag.add(tertiary)


    #Collaboration Factor
    Collaboration = Factor(name="Collaboration",description = "'Collaboration' assesses the extent to which the teacher engages in collaborative problem-solving, shares resources and knowledge, and fosters positive relationships to support student success.",institution = instance)
    Collaboration.save()
    Collaboration.institution_tag.add(primary,secondary,tertiary)
    Collaboration.stakeholder_tag.add(self,teacher,administrator)

    question_27= Question(question="Does the teacher collaborate with colleagues and administrators within their department or grade level team?",factor=Collaboration)
    question_27.save()
    question_27.stakeholder_tag.add(teacher)
    question_27.institution_tag.add(primary,secondary,tertiary)

    question_28= Question(question="Does the teacher contribute positively to team meetings and participate in decision-making processes?",factor=Collaboration)
    question_28.save()
    question_28.stakeholder_tag.add(teacher,administrator)
    question_28.institution_tag.add(primary,secondary,tertiary)

    question_29= Question(question="The teacher respond to feedback and adapt their teaching practices based on input from colleagues?",factor=Collaboration)
    question_29.save()
    question_29.stakeholder_tag.add(teacher,self)
    question_29.institution_tag.add(primary,secondary,tertiary)


    #Instructional Planning Factor
    Instructional_Planning = Factor(name="Instructional Planning",description = "'Instructional Planning' assesses the teacher's ability to plan effective and engaging lessons for their students.",institution = instance)
    Instructional_Planning.save()
    Instructional_Planning.institution_tag.add(primary,secondary,tertiary)
    Instructional_Planning.stakeholder_tag.add(self,teacher,administrator)

    question_30= Question(question="The teacher design assessments and curriculum that accurately measure student learning.",factor=Instructional_Planning)
    question_30.save()
    question_30.stakeholder_tag.add(teacher,administrator)
    question_30.institution_tag.add(primary,secondary,tertiary)

    question_31= Question(question="Do you evaluate the effectiveness of instructional plans and make revisions as needed?",factor=Instructional_Planning)
    question_31.save()
    question_31.stakeholder_tag.add(self)
    question_31.institution_tag.add(primary,secondary,tertiary)

    question_32= Question(question="Do you frequently analyze assessment data to make informed instructional decisions and adjustments?",factor=Instructional_Planning)
    question_32.save()
    question_32.stakeholder_tag.add(self)
    question_32.institution_tag.add(primary,secondary,tertiary)


    #Assessment Factor
    Assessment = Factor(name="Assessment",description = "'Assessment' assesses the teacher's proficiency in analyzing student data, identifying strengths and weaknesses, and using data to inform instructional decisions and improve student outcomes.",institution = instance)
    Assessment.save()
    Assessment.institution_tag.add(primary,secondary,tertiary)
    Assessment.stakeholder_tag.add(self,student,parent)

    question_33= Question(question="The teacher involve students in the assessment process, helping them understand their own strengths and areas for improvement?",factor=Assessment)
    question_33.save()
    question_33.stakeholder_tag.add(self,student)
    question_33.institution_tag.add(secondary,tertiary)

    question_34= Question(question="Does the teacher communicate clearly about your child's progress and areas for improvement?",factor=Assessment)
    question_34.save()
    question_34.stakeholder_tag.add(parent)
    question_34.institution_tag.add(primary)

    question_35= Question(question="Does the teacher provide timely feedback to students on their progress and work?",factor=Assessment)
    question_35.save()
    question_35.stakeholder_tag.add(parent)
    question_35.institution_tag.add(primary)

    question_36= Question(question="Does the teacher provide timely feedback to students on their progress and work?",factor=Assessment)
    question_36.save()
    question_36.stakeholder_tag.add(student)
    question_36.institution_tag.add(secondary,tertiary)

    question_37= Question(question="The teacher treting all students fairly and without bias.",factor=Assessment)
    question_37.save()
    question_37.stakeholder_tag.add(student,self)
    question_37.institution_tag.add(secondary,tertiary)

    question_38= Question(question="The teacher treting all students fairly and without bias.",factor=Assessment)
    question_38.save()
    question_38.stakeholder_tag.add(parent,self)
    question_38.institution_tag.add(primary)

"""