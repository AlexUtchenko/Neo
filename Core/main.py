m = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
n = {"Tuesday": [3,34,5], "Wednesday": [4,4,54], "Monday": [32,23432,4], "Thursday": [4,423,5],  "Tuesday":[324,234,432], "Monday": [2342,234]}
new = []
for i in range(0,5):
    if m[i] in n:
        new.append({m[i]: n[m[i]]})

new2 = [(m[i], n[m[i]]) for i in range(0,5) if m[i] in n]
    
print(new2[0])
