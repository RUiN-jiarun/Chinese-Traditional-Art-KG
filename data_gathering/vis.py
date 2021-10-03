import scrapy
import pymongo
from neo4j import GraphDatabase
import neo4j
import re

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123"), encrypted=False)

db = pymongo.MongoClient("mongodb://127.0.0.1:27017/")["db_wikikg"]["db_triples"]

def add_node(tx, name1, relation, name2):
        tx.run("MERGE (a:Node {name: $name1}) "
               "MERGE (b:Node {name: $name2}) "
               "MERGE (a)-[:"+relation+"]-> (b)",
               name1=name1, name2=name2)

if __name__ == '__main__':
    # TODO: 从数据库中读取entity attr val
    for x in db.find():
        entity = x['sub_name']
        attr = x['attr']
        attr = attr.replace('（', '')
        attr = attr.replace('）', '')
        val = x['obj_name']
        try:
            with driver.session() as session:
                session.write_transaction(
                    add_node, entity, attr, val
                )
        except neo4j.exceptions.CypherSyntaxError:
            print('Syntax Error')