
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
select c.sha1, count(*)  from commit c, merge_commit mc, refactoring r where c.id = mc.id_commit and c.id = r.id_commit group by c.sha1;




























drop database refactoring_merge;
drop database refactoring_merge_t;
create database if not exists refactoring_merge; 
create database if not exists refactoring_merge_t; 



"Deletar projeto - nesta ordem"
delete from refactoring where refactoring.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 3);
delete from merge_branch where merge_branch.id_merge_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 3);
delete from merge_commit where merge_commit.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 3);
delete from commit where id_project = 3;
delete from project where id = 3;



select * from refactoring where refactoring.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 10);
"tabela merge_branch"
select * from merge_branch where merge_branch.id_merge_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 16);
"tabela merge_commit"
select * from merge_commit where merge_commit.id_commit in (select commit.id from commit, project where commit.id_project = project.id and project.id = 16);
"tabela commit"
select * from commit where id_project = 16;
"tabela projeto"
select * from project where id = 16;


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
                          where c.id = mc.id_commit and c.sha1 = 'e78b02fe027621aec1227cbf5555c75775ba296b'))        
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
                           c.sha1 = '563967070a5070e9504d6f2faf78373cd23d33ea') 
        and c.id = r.id_commit and r.type in (select type from refac_accept_type);

563967070a5070e9504d6f2faf78373cd23d33ea |
| 2f1ef083104e352231f6bf0f9e12d37c44a18a9a |
| 7b3d91d145c6e884af5b128f6f1ba518704c46a6 |
| 9d046a1b947d6c262cdc8a584e002d2c4afe0bfe |
| f1773badf14d8dbef599d5ae8d94650a3a2e9792 


#TOTAL COMMITS POR PROJETO
select p.name, count(*) as num_commits from project p, commit c where c.id_project = p.id group by p.name order
by num_commits desc;


#TOTAL MERGE COMMITS POR PROJETO 
select p.name, count(*) as num_merge_commits from project p, commit c, merge_commit mc where c.id_project = p.id and c.id = mc.id_commit group by p.name order by num_merge_commits desc;


#TOTAL MERGE COMMITS POR PROJETO COM FALEID MERGE 
select p.name, count(*) as num_merge_commits from project p, commit c, merge_commit mc
where c.id_project = p.id and c.id = mc.id_commit and mc.extra_effort > 0 
group by p.name order by num_merge_commits desc;

#TOTAL MERGE COMMITS POR PROJETO QUE ENVOLVEM AS 33 REFACS
select p.name, count(*) as num_merge_commits from project p, commit c, merge_commit mc where 
    c.id_project = p.id and c.id = mc.id_commit and (select count(*) from merge_branch mb, commit c1, refactoring r where mb.id_commit = c1.id and 
    mb.id_merge_commit in (select mc.id_commit from merge_commit mc, commit c2 
                          where c2.id = mc.id_commit and 
                           c2.sha1 = c.sha1)
        and c1.id = r.id_commit and r.type in (select type from refac_accept_type)) > 0
    group by p.name order by num_merge_commits desc;







