OBS: MELHORAR DATABASE ############## OBS: Criando do Zero - COLOCAR ON DELETE CASCADE NAS ENTIDADES FRACAS

# Esse merge dá problema no Intellij-community para calcular merge effort. Parar para inevstigar
            db53e5f7fe634aa0db9a012b2125782d76d66d63
            update merge_commit set merge_effort_calculated='True' where id_commit = 1301894;


# mysql -h localhost -u root -p
# abrir o MySQL ===> sudo mysql -u root -p

# backup do bd
mysqldump -u root -p refactoring_merge > refactoring_merge.sql


# restaurar BD - backup do bd
drop database banco_teste_backup
mysql -u root -p banco_teste_backup < refactoring_merge.sql 

########### Dicas de quando dá uma travada no MySQL
This error occurs due to multiple installations of mysql. Run the command:

ps -A|grep mysql
sudo pkill mysql
ps -A|grep mysqld
sudo pkill mysqld
sudo service mysql restart
mysql -u root -p


##### Queries 

use refactoring_merge;

#### Listar todas as tuplas
select * from project;
select id, sha1, date_time, is_merge_commit, id_project, refminer_timeout from commit;
select count(*) from commit c, project p where c.refminer_timeout = 'True' and c.id_project=p.id and p.name not in ('intellij-community','neo4j','graal','spring-boot');
select id, sha1, date_time, is_merge_commit, id_project from commit where sha1 = "3d52b53b46838d7ebe1d1a4258b88cde3dbaed65";
select id, id_commit, is_fast_forward_merge, extra_effort, wasted_effort, rework_effort, branch1_actions, branch2_actions, merge_actions  from merge_commit;
select id, type, id_commit from refactoring;
select refactoring.type from refactoring, commit where refactoring.id_commit = commit.id and commit.sha1 = "7454526686afe3509e8472643beead42d1d4e24c";
select count(*) from merge_commit where is_fast_forward_merge = 'True';
select count(*) from merge_commit where has_base_version = 'False';
select count(*) from merge_commit where has_base_version = 'True' and is_fast_forward_merge = 'False';

### Verificar commits de merge em duplicidade
select commit.sha1, count(*) as total_repetido from merge_commit, commit where commit.id = merge_commit.id_commit and merge_commit.has_base_version = 'True' and merge_commit.is_fast_forward_merge = 'False' group by commit.sha1 having count(*) > 1;
select project.path_workdir, project.name from project, commit where commit.id_project = project.id and commit.sha1 = '5334e80d46de7e5a7a314e6de6423f280f121611';
#########################################

### Qtd de merges Validos de um projeto ####
select p.name, count(*) from project p, commit c where p.id = c.id_project group by p.name order by p.name;
select p.name, count(*) from project p, merge_commit m, commit c where p.id = c.id_project and m.id_commit = c.id group by p.name order by p.name;
select p.name, count(*) from project p, merge_commit m, commit c where p.id = c.id_project and m.id_commit = c.id and m.is_fast_forward_merge='False' group by p.name order by p.name;
select p.name, count(*) from project p, merge_commit m, commit c where p.id = c.id_project and m.id_commit = c.id and m.is_fast_forward_merge='True' group by p.name order by p.name;
#########################################

select commit.id, id_commit, is_fast_forward_merge, extra_effort, wasted_effort, rework_effort, branch1_actions, branch2_actions, merge_actions  from merge_commit, commit, project where project.id = commit.id_project and commit.id = merge_commit.id_commit;

select count(*) from merge_commit where extra_effort > 0 or wasted_effort > 0 or rework_effort > 0;

"""retornar a quantidade de refactorings por TIPO """
select type, count(*) as qty from refactoring group by type order by qty desc;
"""retornar a quantidade de refactorings por TIPO - Só pega os 33 tipos selecionados e vinculados a projetos """
select r.type, count(*) as qty from refactoring r, commit c, project p where r.id_commit = c.id and c.id_project = p.id and r.type in (select type from refac_accept_type) group by r.type order by qty desc;


"""retornar a quantidade de refactorings por id do projeto """
select refactoring.type, count(*) as qty from project, commit, refactoring where project.id = 2 and project.id = commit.id_project and commit.id = refactoring.id_commit group by type order by qty desc;

"""Selecionar da quantidade de refatorações por tipo por commit - via sha1"""
select refactoring.type, count(*) as qty from commit, refactoring where commit.sha1 = "2f21db0b434f6889caaa1550c6b35691065e3df5" and commit.id = refactoring.id_commit group by type order by qty desc;

"""Selecionar da quantidade de refatorações por tipo por commit - via id-commit"""
select refactoring.type, count(*) as qty from commit, refactoring where commit.id = 874 and commit.id = refactoring.id_commit group by type order by qty desc;

"""verificar se é um commit de merge"""
select is_merge_commit from commit where id = 120274;

"""Selecionar commits nos branches de um merge """
select merge_branch.id_merge_commit, (select commit.sha1 from commit where id = merge_branch.id_commit) as sha1, (select commit.date_time from commit where id = merge_branch.id_commit) as date_time , merge_branch.id_commit, merge_branch.type_branch from commit, merge_branch where commit.sha1 = "f88a9502a586b5562059e1a2364bdae10e8f9fd1" and commit.id = merge_branch.id_merge_commit;

""" Verificar commit duplicados """
select c.sha1, count(c.sha1) from commit c, project p where p.id = c.id_project group by c.sha1 having count(c.sha1) > 1;
        """OBS-Antes de apagar os commits simples - ver quais estão ligados ao commit_de_merge e apagar esse primeiro"""
select c.sha1 from merge_commit m, commit c where m.id_commit = c.id group by c.sha1 having count(c.sha1) > 1;

""" DUPLICOU esse cara tem refatoraçõe iguais nos dois commits 2e06545a9eb2ceee08e24e63e696fb0bec940ff0
VER COMO FICOU NOS BRANCHES - se um deles não for mencionado no branch - excluir
 """



select * from merge_branch;

ALTER TABLE merge_commit CHANGE extra_effort extra_effort bigint;
ALTER TABLE commit CHANGE author author varchar(200)
ALTER table commit add column refminer_timeout enum('False', 'True') DEFAULT 'False' NOT NULL after parent;
ALTER table merge_commit add column merge_effort_calculated enum('False', 'True') DEFAULT 'True' NOT NULL after is_fast_forward_merge;

#### UPDATE ####
update project set name = 'druid' WHERE id = 15;
update project set path_workdir = '/mnt/c/Users/aoliv/RepositoriosEO1/druid/' WHERE id = 15;

### Selecionar merge branch de um projeto específico ######
select mb.id_commit, mb.id_merge_commit, mb.type_branch, c.sha1 from merge_branch mb, commit c, project p where mb.id_commit = c.id and c.id_project = p.id and p.path_workdir = '/mnt/c/Users/aoliv/RepositoriosEO1/hadoop/' order by mb.id_merge_commit;

### exibir projetos que ainda não computaram MERGE EFFORT ######
select p.path_workdir, count(*) from merge_commit m, project p, commit c where m.merge_effort_calculated = 'False' and p.id = c.id_project and m.id_commit = c.id group by p.path_workdir;
select m.extra_effort, m.wasted_effort, m.rework_effort, m.merge_effort_calculated from project p, commit c, merge_commit m where p.id = c.id_project and c.id = m.id_commit and p.path_workdir = '/mnt/c/Users/aoliv/RepositoriesGiHub/refactoring-toy-example/';
select m.extra_effort, m.wasted_effort, m.rework_effort, m.merge_effort_calculated, m.branch1_actions, m.branch2_actions, merge_actions from project p, commit c, merge_commit m where p.id = c.id_project and c.id = m.id_commit and p.path_workdir = '/mnt/c/Users/aoliv/RepositoriosEO1/spring-boot/'and m.merge_effort_calculated='True' and m.extra_effort<>0;

#### Total de commits no-ff por projeto ####
select p.path_workdir, count(*) from merge_commit m, commit c, project p where p.id = c.id_project and m.id_commit = c.id and m.is_fast_forward_merge = 'True' group by p.path_workdir order by p.path_workdir;

#### Total de commits de merge válidos por projeto ####
select p.path_workdir, count(*) from merge_commit m, commit c, project p where p.id = c.id_project and m.id_commit = c.id and m.is_fast_forward_merge = 'False' group by p.path_workdir order by p.path_workdir;

#### Total de commit com refatorações em um dado projeto ####
select count(distinct c.sha1) as total_commits_with_refac from commit c, refactoring r where c.id = r.id_commit and c.id_pro
ject = 80;


########################################################

create table duplicidade_id(
    id bigint
);

create table duplicidade_sha1(
    sha1 varchar(40) NOT NULL    
);

create table duplicidade_sha1_2(
    sha1 varchar(40) NOT NULL,
    id bigint
);

"""DELETAR DUPLICIDADE NA TABELA DE MERGE COMMIT - POR id"""
insert into duplicidade_id (select id from merge_commit where id in (select m.id from project p, commit c, merge_commit m where p.id = c.id_project and c.id = m.id_commit and p.path_workdir = '/mnt/c/Users/aoliv/RepositoriosEO1/hadoop/' and m.id < (select max(x.id) from merge_commit x where x.id_commit = m.id_commit)));
delete from merge_commit as m where m.id in (select id from duplicidade_id);


"""DELETAR DUPLICIDADE (sha1) NA TABELA DE COMMIT - POR id"""
insert into duplicidade_id (select id from commit where id in (select c.id from project p, commit c where p.id = c.id_project and p.path_workdir = '/mnt/c/Users/aoliv/RepositoriosEO1/intellij-community/' and c.id < (select max(x.id) from commit x where x.sha1 = c.sha1)));


delete from commit as m where m.id in (select id from duplicidade_id);



































drop database refactoring_merge;
drop database refactoring_merge_t;
create database if not exists refactoring_merge; 
create database if not exists refactoring_merge_t; 



"Deletar projeto - nesta ordem"
#tabela refactoring
delete from refactoring where refactoring.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 17);
#tabela merge_branch
delete from merge_branch where merge_branch.id_merge_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 17);
#tabela merge_commit
delete from merge_commit where merge_commit.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 17);
#tabela commit
delete from commit where id_project = 17;
#tabela projeto
delete from project where id = 17;



select * from refactoring where refactoring.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 17);
"tabela merge_branch"
select * from merge_branch where merge_branch.id_merge_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 17);
"tabela merge_commit"
select * from merge_commit where merge_commit.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 17);
"tabela commit"
select * from commit where id_project = 17;
"tabela projeto"
select * from project where id = 17;


// PESQUISA FEITA PARA O ARTIGO 1 - INSPEÇÂO MANUAL

select distinct c.sha1 from project p, commit c, merge_commit mc, refactoring r where
 p.id = c.id_project and c.id = mc.id_commit and  c.id = r.id_commit 
 and r.type in ('Extract Method','Inline Method','Pull Up Method','Push Down Method') 
 and p.name in ('Activiti','netty','elasticsearch') and mc.extra_effort >=2  and mc.extra_effort <20;


select r.type from commit c, refactoring r where c.id = r.id_commit and c.sha1="e051b5f338c3f7b722a65d2dd1ee36178b44dfdd";

//OTIMA retorna total de accepted refacs por commit
select r.type, count(*) from commit c, refactoring r where c.id = r.id_commit and c.sha1="2dbf860ac4e693bfa06448a8d080a361676d6a3b" and r.type in (select type from refac_accept_type) group by r.type order by r.type; 

//NINJA: Variação da de cima pegando as refacs de todos os commits dos ramos
select r.type, count(*) from commit c, refactoring r where 
        c.id = r.id_commit and r.type in (select type from refac_accept_type) 
        and c.id in (select distinct(c.id) from merge_branch mb, commit c, refactoring r where mb.id_commit = c.id and 
                        mb.id_merge_commit in (select mc.id_commit from merge_commit mc, commit c 
                          where c.id = mc.id_commit and c.sha1 = '6c0d2cb4c21d1d0c5fa1570f9d99b4927801e519'))        
        group by r.type order by r.type;

//and c.id not in (select mc.id_commit from merge_commit mc)

//pegar commits nos ramos deste commit que tenham um dos 4 tipos de refactorings consideradas
select distinct c.sha1 from merge_branch mb, commit c, refactoring r where mb.id_commit = c.id and 
    mb.id_merge_commit in (select mc.id_commit from merge_commit mc, commit c where c.id = mc.id_commit and
     c.sha1 = 'd7086e1635269f51b25d67479dc045a991a51606') and c.id = r.id_commit and 
     r.type in ('Extract Method','Inline Method','Pull Up Method','Push Down Method');


//Query MUITO IMPORTANTE
//pegar commits nos ramos deste commit que tenham um dos 33 tipos de refactorings consideradas
select distinct(c.sha1), type_branch from merge_branch mb, commit c, refactoring r where mb.id_commit = c.id and 
    mb.id_merge_commit in (select mc.id_commit from merge_commit mc, commit c 
                          where c.id = mc.id_commit and 
                           c.sha1 = '6c0d2cb4c21d1d0c5fa1570f9d99b4927801e519') 
        and c.id = r.id_commit and r.type in (select type from refac_accept_type);


