from subprocess import call

# Asking for user choice

user_choice = input("Please enter numerical or label (default is numerical): ")

   
if user_choice == "label":
   print('User choice: ',user_choice)
   instruction = input("Enter instruction in the format 'python label.py N --options True': ")
   call (instruction, shell = True)

else:
    user_choice = "numerical"
    print("User choice is:", user_choice)
    instruction = input("Enter instruction in the format 'python numerical.py example_data/filename.txt --options True': ")
    call (instruction, shell = True)


