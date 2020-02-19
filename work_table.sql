SELECT classes.name_classes AS "Номер класса", 
	   subject.name_subject AS "Предмет",
	   teachers.name_teachers AS "ФИО учителя",
	   teachers.qualification AS "Квалификация"
FROM learningactivities
JOIN classes ON learningactivities.number_classes = classes.id
JOIN subject ON learningactivities.name_subject = subject.id
JOIN teachers ON learningactivities.name_teachers = teachers.id