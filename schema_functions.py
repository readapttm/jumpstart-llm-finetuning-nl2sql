
from operator import itemgetter
from copy import deepcopy


def create_schema(tables_list: list) -> dict:

    """
    This function takes a list of tables and returns a schema for a database

    Args:
        tables_list (list): list of tables

    Returns:
        tables (dict): formatted schema
    """

    tables = dict()

    # Loop through each dataset in training set
    for table_temp in tables_list:
        table_formatted = []

        # For each table, list column names and types
        for i, t in enumerate(table_temp['table_names_original']):
            
            table_formatted.append({'table_name': t})
            table_formatted[i]['columns'] = [{'column_name': c[1],
                                'column_type': p} 
                                for c, p in zip(table_temp['column_names_original'], table_temp['column_types']) if c[0] == i]
        
        # Extract primary keys
        for j, p_list in enumerate(table_temp['primary_keys']):
            if type(p_list) == int:
                p_list = [p_list]

            table_formatted[j]['primary_keys'] = itemgetter(*p_list)(table_temp['column_names_original'])

        # Extract foreign keys
        for k, f_list in enumerate(table_temp['foreign_keys']):
            
            keys = itemgetter(*f_list)(table_temp['column_names_original'])

            for k_id in keys:
                
                opp = [a for a in keys if a != k_id][0]
                
                if 'foreign_keys' not in table_formatted[k_id[0]].keys():
                    table_formatted[k_id[0]]['foreign_keys'] = dict()
                
                table_formatted[k_id[0]]['foreign_keys'].update({k_id[1]: {table_temp['table_names_original'][opp[0]]: opp[1]}})

        tables[table_temp['db_id']] = table_formatted


    ## Ensure single entry primary keys are lists
    for k, v in tables.items():

        for b in v:

            if b.get('primary_keys') is not None and len(b.get('primary_keys')) == 2 and type(b.get('primary_keys')[0]) == int:
                b['primary_keys'] = [b['primary_keys']]


    # Select only primary key column name
    for k, v in tables.items():

        for b in v:
            # b = v[0]
            if b.get('primary_keys') is not None:            
                b['primary_keys'] = [p[1] for p in b['primary_keys']]

    return tables



def abbreviate_schema(schema: dict) -> dict:

    """
    This function takes a schema dictionary and reformats it to require fewer tokens

    Args:
        schema (dict): a database schema

    Returns:
        new_schema (dict): abbreviated version of input schema
    """

    schema = deepcopy(schema)

    new_schema = dict()

    for k, v in schema.items():

        table_dict = {}

        for a in v:
            #a = v[0]
            table_dict[a['table_name']] = a        

        for a in v:
            table_dict[a['table_name']]['columns'] = {c['column_name']:c['column_type'] for c in table_dict[a['table_name']]['columns']}
        
        for _, j in table_dict.items():
            j.pop('table_name') 

        new_schema[k] = table_dict

    return new_schema