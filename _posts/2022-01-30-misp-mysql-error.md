---
layout: post
title:  "MISP MySQL related errors."
date:   2022-01-30
---

# memo



# MISP MySQL related issues.

- [SELECT list is not in GROUP BY clause and contains nonaggregated column 'misp.GalaxyCluster.value' #7013](https://github.com/MISP/MISP/issues/7013)
- [500 error listing attributes and tags #79](https://github.com/coolacid/docker-misp/issues/79)
- [Fix MySQL ONLY_FULL_GROUP_BY #80](https://github.com/coolacid/docker-misp/pull/80)
- [disable the strict mode on mysql 5.7 docker build file #149](https://github.com/docker-library/mysql/issues/149)

# Error log

I'm having the same issue. (on docker misp(ver. 2.4.152))
'Event actions -> Events with proposal' also has same problem. The error.log is as follows.

```
2022-01-30 10:41:55 Error: [PDOException] SQLSTATE[HY000]: General error: 3065 Expression #2 of ORDER BY clause is not in SELECT list, references column 'misp.ShadowAttribute.type' which is not in SELECT list; this is incompatible with DISTINCT
Request URL: /events/proposalEventIndex
Stack Trace:
#0 /var/www/MISP/app/Lib/cakephp/lib/Cake/Model/Datasource/DboSource.php(502): PDOStatement->execute()
#1 /var/www/MISP/app/Lib/cakephp/lib/Cake/Model/Datasource/DboSource.php(468): DboSource->_execute()
#2 /var/www/MISP/app/Lib/cakephp/lib/Cake/Model/Datasource/DboSource.php(715): DboSource->execute()
#3 /var/www/MISP/app/Lib/cakephp/lib/Cake/Model/Datasource/DboSource.php(1226): DboSource->fetchAll()
#4 /var/www/MISP/app/Lib/cakephp/lib/Cake/Model/Model.php(3053): DboSource->read()
#5 /var/www/MISP/app/Lib/cakephp/lib/Cake/Model/Model.php(3025): Model->_readDataSource()
#6 /var/www/MISP/app/Controller/EventsController.php(3351): Model->find()
#7 [internal function]: EventsController->proposalEventIndex()
#8 /var/www/MISP/app/Lib/cakephp/lib/Cake/Controller/Controller.php(499): ReflectionMethod->invokeArgs()
#9 /var/www/MISP/app/Lib/cakephp/lib/Cake/Routing/Dispatcher.php(193): Controller->invokeAction()
#10 /var/www/MISP/app/Lib/cakephp/lib/Cake/Routing/Dispatcher.php(167): Dispatcher->_invoke()
#11 /var/www/MISP/app/webroot/index.php(99): Dispatcher->dispatch()
#12 {main}
```

```
mysql > SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
```


```
root@7d6426382391:/var/www/MISP# mysql -u misp -p
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 479
Server version: 5.7.37 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]> SELECT @@global.sql_mode;
+-------------------------------------------------------------------------------------------------------------------------------------------+
| @@global.sql_mode                                                                                                                         |
+-------------------------------------------------------------------------------------------------------------------------------------------+
| ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+-------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)

MySQL [(none)]> 
```

```
mysql > SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
```