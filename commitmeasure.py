from pydriller import RepositoryMining


'''
filepath ="/home/ask/Git/tweeda/Main.py"
filename = filepath.split('/')[-1]

linesChanged = 0 
linesdeleted = 0
linesAdded = 0

for commit in RepositoryMining("/home/ask/Git/tweeda", filepath=filepath).traverse_commits():
    # here you have the commit object


    for m in commit.modifications:
        if (filename == m.filename):
            print(m.new_path)
            linesdeleted = linesdeleted + m.removed
            linesAdded = linesAdded = m.added
            linesChanged = linesChanged = m.changed_methods # this is not correct, but how do I acces modified lines?


churn = linesChanged + linesAdded + linesdeleted

print(churn)
'''
churn_per_file = {}
for commit in RepositoryMining("/home/ask/Git/Zeeguu-API").traverse_commits():
    for modified_file in commit.modifications:
        churn = modified_file.removed + modified_file.added
        if modified_file.new_path not in churn_per_file: # Here you should keep track of renaming, add a new "if-else"
            churn_per_file[modified_file.new_path] = 0
        churn_per_file[modified_file.new_path] = churn_per_file[modified_file.new_path] + churn



for k,v in churn_per_file.items():
    print("k: " + str(k) + "  value: "  + str(v))

print("herherherh: " + str(churn_per_file["zeeguu_api/api/feature_toggles.py"]))