import asana
import os 
import re

#init

client = asana.Client.access_token(os.environ['ASANA_ACCESS_TOKEN'])
workspaces = client.workspaces.find_all()
projects = client.projects.find_all({'workspace': list(workspaces)[0]["gid"]})

#fonctions

#on récupère les différents projets au sein de chaintrust 

def find_project_id_by_name(projects):
    result_projects = []
    for project_name in projects_list : 
        if project_name == projects["name"]:
            result_projects.append(projects['gid'])
    return result_projects

#On cherche les tâches des différents projets

def find_task_id_by_name(projects):
    result_task = []
    all_tasks = client.tasks.find_all({'project': projects})
    for task in all_tasks: 
        if task_name in task['name']:
            result_task.append({'project': projects[0], 'task': task['gid']})
    return result_task
    
#On cherche dans quelles sections sont les tâches et on les bouge 
    
def find_state_id_by_name(tasks):
    result_state = []
    sections = client.sections.find_by_project(tasks['project'])
    for section in sections:
        if new_state_of_task in section['name']:
            client.sections.add_task(section['gid'], {'task': tasks['task']})
            result_state.append(task_name + ' move to ' + new_state_of_task)
    return result_state


#Script 

name_PR = os.environ['PR_NAME']
is_merge = os.environ['PR_MERGE']
if (is_merge == 'true'):
    new_state_of_task = 'Merged in main' 
else: 
    new_state_of_task = 'In review' 


#A modifier à la mano 
typology_name = ['ops', 'bus', 'cli']
projects_list = ["Tech · Intra", "Tech · Extra"] 


def move_task():
    for typo in typology_name:     #on check le nom de la task 
        if(typo in task_name.lower()):
            result_projects = list(filter(None, list(map(find_project_id_by_name, list(projects)))))
            if result_projects == []: 
                return "Vous n'avez accès à aucun projet sur asana"
            else: 
                result_task = list(filter(None, map(find_task_id_by_name, result_projects)))
                if result_task == []: 
                    return "Vous n'avez aucune tâche de ce nom dans vos projets asana"
                else: 
                    result = list(map(find_state_id_by_name, result_task[0]))
                    if result == []:
                        return "Aucune tâche n'a pu être bougée"
                    else: 
                        return result
        else:
            return 'le nom de la tâche n\'est pas valide'


name = re.search('(.+?)-', name_PR)
if name:
    task_name = (''.join(name.group(1).split()))
    print(move_task())
else: 
    print('le nom de la PR n\'est pas valide')

