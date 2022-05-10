import asana
import os 
import re

#init

client = asana.Client.access_token(os.environ['ASANA_ACCESS_TOKEN'])
workspaces = client.workspaces.find_all()
all_projects = list(client.projects.find_all({'workspace': list(workspaces)[0]["gid"]}))

###fonctions

#On cherche les tâches des différents projets

def find_task_id_by_name(project_gid, task_tag):
    result_task = []
    all_tasks = list(client.tasks.find_all({'project': project_gid}))
    for task in all_tasks: 
        if task_tag in task['name'].lower():
            result_task.append({'project': project_gid, 'task': task['gid']})
    return result_task
     

#Move task  

def move_task_section(task_tag, task, new_state_of_task):
    result_state = []
    sections = client.sections.find_by_project(task['project'])
    for section in sections:
        if new_state_of_task in section['name']:
            client.sections.add_task(section['gid'], {'task': task['task']})
            result_state.append(task_tag + ' move to ' + new_state_of_task)
    return result_state
                   
#move_task_to_new_state

def move_task_to_new_state(task_tag, new_state_of_task):
    projects = [project['gid'] for project in all_projects if project['name'] in projects_list]     #on récupère les projets comportant le nom de la PR  
    if projects == []: 
        print("Vous n'avez accès à aucun projet sur asana")
        exit(1)
    else: 
        result_task = [find_task_id_by_name(project, task_tag) for project in projects] #on récupère les tâches dans les projets 
        if result_task == []: 
            print("Vous n'avez aucune tâche de ce nom dans vos projets asana")
            exit(1)
        else: 
            result = [move_task_section(task_tag, task, new_state_of_task)  for tasks_per_projects in result_task for task in tasks_per_projects]
            if result == []:
                print("Aucune tâche n'a pu être bougée")
                exit(1)
            else: 
                print(result)     

def check_name(task_tag, typology_name):
    typology = None
    for typo in typology_name:  
        if(typo in task_tag):             
            typology = typo
    
    if (typology == None):
        print('le nom de la PR n\'est pas valide')
        return False
    else: 
        return True

#A modifier à la mano 

typology_name = ['ops', 'bus', 'cli']
projects_list = ["Tech · Intra", "Tech · Extra"] 


#recup info github

name_PR = os.environ['PR_NAME'] if "PR_NAME" in os.environ else None
is_merge = os.environ['PR_MERGE'] if "PR_MERGE" in os.environ else None
pr_nb_deploy = os.environ['PR_NB_FOR_DEPLOY'] if "PR_NB_FOR_DEPLOY" in os.environ else None
repo_name = os.environ['REPO_NAME'] if "REPO_NAME" in os.environ else None

if (pr_nb_deploy): 
    new_state_of_task = 'Producted'
elif (is_merge == 'true'):
    new_state_of_task = 'Merged in main' 
else: 
    new_state_of_task = 'In review'     

if (pr_nb_deploy != "" and is_merge == 'true'):  #1e cas : deploy

    from github import Github
    g = Github(os.environ['GITHUB_TOKEN'])
    repository = None

    print(g.get_repo(f"chaintrust-app/{repo_name}"))
    #for repo in g.get_user().get_repos():
        # if (repo.name == repo_name):
        #     repository = repo
    repository = g.get_repo(f"chaintrust-app/{repo_name}")
    if(repository == None): 
        print('le repo n\'existe pas')
        exit(1)
    else: 
        print(repository)

    pr_deploy = repository.get_pull(int(pr_nb_deploy))
    list_commits = list(pr_deploy.get_commits())

    list_message_commit = []
    for commit in list_commits: 
        list_message_commit.append(commit.commit.message)

    # list_message_commit = ['Merge pull request #2113 from chaintrust-app/pc/backport-acd-fix', 'PM create table legal entities event', 'Merge pull request #2089 from chaintrust-app/fix_spam_error_toaster_for_customer_GED', 'feat(pick_merchant): add start picking endpoint', 'feat(pick merchant): add pricing set']
    # print(list_message_commit)

    pr_titles = []

    for message in list_message_commit:
        name = re.search('Merge pull request #(.+?) ', message)
        if name : 
            number = re.search('#(.+?) ', message)
            PR_nb = (''.join(number.group(1).split())).lower()
            pr = repository.get_pull(int(PR_nb))
            pr_titles.append(pr.title)

    print(pr_titles)
    for title in pr_titles:
        name = re.search('(.+?)-', title)
        if name:
            task_tag = (''.join(name.group(1).split())).lower()
        else: 
            print('le nom de la PR n\'est pas valide')
            exit(1)

        if check_name(task_tag, typology_name):
            move_task_to_new_state(task_tag, new_state_of_task)
        else: 
            print('le nom de la PR n\'est pas valide')
            exit(1)   

else: #2e cas : si in review ou merge in main 
    name = re.search('(.+?)-', name_PR)
    if name:
        task_tag = (''.join(name.group(1).split())).lower()
    else: 
        print('le nom de la PR n\'est pas valide')
        exit(1)

    if check_name(task_tag, typology_name):
        move_task_to_new_state(task_tag, new_state_of_task)
    else: 
        print('le nom de la PR n\'est pas valide')
        exit(1)   
