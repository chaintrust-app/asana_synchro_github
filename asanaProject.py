import asana
import os 
import re
from entrypoint.sh import test_name 
print(test_name)

print(os.environ['ASANA_ACCESS_TOKEN'])

################ info Github
name_PR = '  OPS111 1- PR test de github'
new_state_of_task = 'In review'

new_state_current_task = '1201905760894304'

#si plusieurs => faire bouger les 2

################ info Asana
client = asana.Client.access_token(os.environ['ASANA_ACCESS_TOKEN'])

#l'espace chaintrust sur asana
workspaces = client.workspaces.find_all()
workspace_id = '1170802161750680'

#les différents projets au sein de chaintrust 
projects = client.projects.find_all({'workspace': workspace_id})

#Ici, je test sur tech-Intra
tech_intra_id = 1201905678510288
tasks = client.tasks.find_all({'project': tech_intra_id})
sections = client.sections.find_by_project(tech_intra_id)

##################script 

#On cherche la task associée sur asana 

###valider le nom 

task_name = (''.join(re.search('(.+?)-', name_PR).group(1).split()))

def find_task_id_by_name(tasks):
    if task_name in tasks['name']:
        return tasks['gid']
    else : 
        return ''
    
list_tasks_with_id = map(find_task_id_by_name, list(tasks))
current_task = (''.join(list(list_tasks_with_id)))
#print(current_task)

#On cherche la colonne associé sur asana 
    
def find_state_id_by_name(sections):
    if new_state_of_task in sections['name']:
        return sections['gid']
    else : 
        return ''

list_state_with_id = map(find_state_id_by_name, list(sections))
new_state_current_task = (''.join(list(list_state_with_id)))
#print(new_state_current_task)

#on bouge la carte

client.sections.add_task(new_state_current_task, {'task': current_task})


#print(list(tasks))
#print(list(sections))