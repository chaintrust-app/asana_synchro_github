import asana
import os 
import re

################ info Github
name_PR = '  OPS111 1- PR test de github' #os.environ['PR_NAME']
new_state_of_task = 'In review'  ## a checker 

################ info Asana => on récupère les différents projets au sein de chaintrust 

client = asana.Client.access_token(os.environ['ASANA_ACCESS_TOKEN'])
workspaces = client.workspaces.find_all()
projects = client.projects.find_all({'workspace': list(workspaces)[0]["gid"]})

projects_list = ["Tech · Intra", "Tech · Extra", "Roadmap"] #verifier qu'on a accès 


def find_project_id_by_name(projects):
    result_projects = []
    for project_name in projects_list : 
        if project_name == projects["name"]:
            result_projects.append(projects['gid'])
    return result_projects

result_projects = list(filter(None, list(map(find_project_id_by_name, list(projects)))))
print(result_projects)

##si on a rien => ???

##################script 

#valider le nom 

typology_name = ['ops', 'bus', 'cli']
task_name = (''.join(re.search('(.+?)-', name_PR).group(1).split()))

for typo in typology_name:
    if(typo in task_name.lower()):
        print('coool')
    
##sinon => ???


#On cherche les tâches des différents projets

def find_task_id_by_name(projects):
    result_task = []
    all_tasks = client.tasks.find_all({'project': projects})
    print(projects)
    for task in all_tasks: 
        if task_name in task['name']:
            result_task.append({task['gid']: projects})
    print(result_task)
    return result_task
    
result_task = filter(None, list(map(find_task_id_by_name, result_projects)))
print(list(result_task)) #current task 

#On cherche dans quel section sont les tâches et on les bouge 

sections = client.sections.find_by_project(1201905678510288)

#On cherche la colonne associé sur asana 
    
def find_state_id_by_name(sections):
    if new_state_of_task in sections['name']:
        return sections['gid']
    else : 
        return ''

result_state = map(find_state_id_by_name, list(sections))
new_state_current_task = (''.join(list(result_state)))

#on bouge la carte

#client.sections.add_task(new_state_current_task, {'task': current_task})


#print(list(tasks))
#print(list(sections))