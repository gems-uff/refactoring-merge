
import pygit2
import os, stat
import time
from datetime import datetime
from datetime import date
import time
import json
import subprocess


# Pré-requisitos - Instalar o pygit2

#### ####################################################################################
print(bool(pygit2.features & pygit2.GIT_FEATURE_SSH))

#### ####################################################################################
# SETAR OS DADOS DO USUÁRIO GitHub
username = 'aoliveira100'
password = 'samba@98'
credentials = pygit2.UserPass(username, password)
callbacks = pygit2.RemoteCallbacks(credentials=credentials)

#### ####################################################################################
# SETAR O REPOSITÓRIO GitHub
repo_url = 'https://github.com/gems-uff/refactoring-merge.git'


#### ####################################################################################
# SETAR O DIRETÓRIO ONDE OS PROJETOS SERÃO CLONADOS
current_working_directory = os.getcwd()
print(current_working_directory)
os.chmod(current_working_directory, stat.S_IRWXO)
repo_path = current_working_directory + "/build/" + str(time.time())

#### ####################################################################################
# ????? CLONAR UM PROJETO - ESTA DANDO ERRO: _pygit2.GitError: failed to mmap. Could not write data: Permission denied
# repo_aux = pygit2.clone_repository(repo_url, repo_path, callbacks=callbacks)

# SETAR O REPOSITÓRIO
# repo_path = repo_aux.workdir
# repo = pygit2.Repository(repo_path)
# repo.describe()


#### ####################################################################################
# DESCOBRIR UM REPOSITÓRIO
repo_path = pygit2.discover_repository("/mnt/c/Users/aoliv/refactoring-merge/mergeeffort/build/refactoring-toy-example")
# https://github.com/PipedreamHQ/pipedream.git
repo = pygit2.Repository(repo_path)
print(repo)

# Pegar o último commit
last_commit = repo[repo.head.target]
print(last_commit)

#### ####################################################################################
# Caminhando pelos commits do repositório - do último Commit até uma constante pygit2.GIT_SORT_TOPOLOGICAL 
# Colocar os dados dos commits em um Dictionary
commits = {}
for commit in repo.walk(last_commit.id, pygit2.GIT_SORT_TOPOLOGICAL):     
    commit_data = {'message': commit.message, 'author': commit.author.name, 'parents': commit.parents, 'date_time': datetime.fromtimestamp(commit.commit_time), 'visited': False}
    # print(dir(commit))    
    # print(commit_data)    
    # break       
    commits[str(commit.id)] = commit_data     

# print(commits)
# print(f" Commit - Imprimir Dados: {commits['e1ad0a065ed20bbea38547b728158c50029a4303']}")
# print(f" Commit - Imprimir Dados: {commits['5d44fa886bcb51e8f595915fa85d506e9dee3e8c']}")

#### ####################################################################################
#### contar quantos commits
print(f"quantidade de commits = {len(list(repo.walk(last_commit.id)))}")

#### ####################################################################################
#### Pegar os commits de todos os branches
branches_list = list(repo.branches)
# print(f"Branches: {branches_list}")
# Local only
local_branches_list = list(repo.branches.local)
# print(f"Local Branches: {local_branches_list}")
# Remote only
remote_branches_list = list(repo.branches.remote)
# print(f"Remote Branches: {remote_branches_list}")
# Get a branch
branch_master = repo.branches['master']


#### ####################################################################################
# retorna um conjunto (set) com os commits de merge
def merge_commits(commits):
	""" Gets all reachable merge commits from a set of commits """
	visited = set()
	merges = set()

	while commits:
		commit = commits.pop()
		if commit.id not in visited:
			visited.add(commit.id)
			commits.update(commit.parents)
			if len(commit.parents) == 2:
				merges.add(commit)

	return merges

#### ####################################################################################
# incluir em uma lista todos os commits de merge
commits_merge = []
commits_merge = list(merge_commits({repo.branches[branch_name].peel() for branch_name in repo.branches}))
print(len(commits_merge))

print(dir(commits_merge[0]))

#for commit in commits_merge:
#	print(commit.id)

#### ####################################################################################
# Gerar um Json com os commits de merge

list_commits = []
for commit in commits_merge:
   commit_data = {'sha': str(commit.id), 'date_time': str(datetime.fromtimestamp(commit.commit_time)), 'message': commit.message, 'author': commit.author.name} 
   list_commits.append(commit_data)   

list_commits_json = json.dumps(list_commits)
# print(list_commits_json)

with open('commits_merge.json', 'w') as json_file:
    json.dump(list_commits, json_file, indent=4)

############################################################
#  Listar commits por branch

# print(dir(repo))

i = 0
commits_ordenados = []
for branch_name in repo.branches:
	if(i==0):
		print(f"{branch_name} - {repo.branches[branch_name].peel()}")
		j = 0
		for commit in repo.walk(repo.branches[branch_name].peel().id,pygit2.GIT_SORT_REVERSE):
			commits_ordenados.append(commit)
			if(j<2):
				print(f"{commit.id} - {str(datetime.fromtimestamp(commit.commit_time))}")
			j = j +1		
	i = i+1
print(f"Lista de commits ordenados pelo tempo = {len(commits_ordenados)}")
#for c in commits_ordenados:
#	print(f"{c.id} - {str(datetime.fromtimestamp(c.commit_time))}")

commits_merge = []
for commit in commits_ordenados:
	if len(commit.parents) == 2:
		commits_merge.append(commit)


print(f"Total de commits = {len(commits_ordenados)} Commit de merge = {len(commits_merge)}")
j= 0
visited = set()
for commit in commits_merge:
	if(j==6):
		print(f"Commit de merge = {commit.id} - {str(datetime.fromtimestamp(commit.commit_time))}")
		print(f"Pai-1 = {commit.parents[0].hex}")
		print(f"Pai-2 = {commit.parents[1].hex}")
		commum_ancestral = repo.merge_base(commit.parents[0].hex, commit.parents[1].hex)
		print(f"Ancestral Comum = {commum_ancestral}")
		parent1_list = []
		commit_evaluate = commit.parents[0]
		""" para estar na lista tem que respeitar 3 criterios:
			1) não ser o ancetral comum dos branches
			2) não ser um commit de merge
			3) não ter sido visitado
		"""			
		while commit_evaluate.hex != commum_ancestral.hex and len(commit_evaluate.parents)==1 and commit_evaluate.id not in visited:
			visited.add(commit_evaluate.id)
			parent1_list.append(commit_evaluate)
			commit_evaluate = commit_evaluate.parents[0]

		print(parent1_list)

		parent2_list = []
		commit_evaluate = commit.parents[1]		
		""" para estar na lista tem que respeitar 3 criterios:
			1) não ser o ancetral comum dos branches
			2) não ser um commit de merge
			3) não ter sido visitado
		"""			
		while commit_evaluate.hex != commum_ancestral.hex and len(commit_evaluate.parents) ==1 and commit_evaluate.id not in visited:
			visited.add(commit_evaluate.id)
			parent2_list.append(commit_evaluate)
			commit_evaluate = commit_evaluate.parents[0]
		
		print(parent2_list)	


	j = j+1


	#print(repo.path)

## OBS: peel() retorna o último commit de cada branch. A partir daí é possível navegar no caminho contrário


# https://docs.python.org/2/library/subprocess.html#module-subprocess
# Fazer o clone do projeto Refactoring Miner
# precisa do java instalado na máquina
# sudo apt-get update
# java -version
# sudo apt-get install default-jre
# sudo apt-get install default-jdk
# entrar na pasta do Refactoring Miner clonado e executar o arquivo ./gradlew distZip
# descompactar o arquivo /RefactoringMiner/build/distributions/RefactoringMiner-2.1.0.zip
# sudo apt install zip unzip
# unzip RefactoringMiner-2.1.0.zip
# executar o comando  RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner
# Exemplo
	# sudo /mnt/c/Users/aoliv/refactoring-merge/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner -c /mnt/c/Users/aoliv/refactoring-merge/mergeeffort/build/pipedream bdfdc017159ac064d94d1bb2f46601f6b0443b7d  -json refactoring.json


# executar meu programa 
# sudo python3 ./merge_refactoring_analysis.py --repo_path /mnt/c/Users/aoliv/refactoring-merge/mergeeffort/build/pipedream --output_path mnt/c/Users/aoliv/refactoring-merge/mergeeffort/build



"""
refMiner_exec = "/mnt/c/Users/aoliv/refactoring-merge/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner"
# Carrega um arquivo json e coloca em um dict
def read_json(arq_json):
    with open(arq_json, 'r', encoding='utf8') as f:
        return json.load(f)

def write_json(data,file_name):			
	with open(file_name, 'w', encoding='utf-8') as json_file:
		json.dump(data, json_file, ensure_ascii=False, indent=4)

def get_refactoring_commit(path_repository,commit_sha1):		
	print(commit_sha1)
	subprocess.call(refMiner_exec + " -c " + path_repository + " " + str(commit_sha1) + " -json " + "ref_miner_temp.json", shell=True)
	retorno_arq = read_json("ref_miner_temp.json")			
	subprocess.call("rm ref_miner_temp.json", shell=True)		
	commit = retorno_arq['commits']
	if len(commit) > 0:
		return commit[0]['refactorings']
	else:
		list_refac = []
		return list_refac


commits_list_refatoring = []
for commit in commits_ordenados:
	print(commit.id)
	commit_data = {
					'sha1': str(commit.id),					
					'refactorings' : get_refactoring_commit(repo.workdir, commit.id)					
				  } 
	commits_list_refatoring.append(commit_data)

write_json(commits_list_refatoring,"toy-refactorings.json")
"""


#Video legal Pandas
# https://www.codigofluente.com.br/aula-04-instalando-o-pandas/

