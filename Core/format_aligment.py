grades = {"A": 5, "B": 5, "C": 4, "D": 3, "E": 3, "FX": 2, "F": 1}


def formatted_grades(students):
    global grades
    cnt = 0
    for student, mark in students.items():
        cnt +=1 
        print('{:>4}|{:<10}|{:^5}|{:^5}'.format(cnt, student, mark, grades[mark]))
    
    
    
        
        
students = {"Nick": "A", "Olga": "B", "Mike": "FX", "Anna": "C"}      
formatted_grades(students)