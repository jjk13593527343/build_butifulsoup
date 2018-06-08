# -*- encoding:utf-8 -*-
import bs4
from bs4 import BeautifulSoup
import json

def create_class_instance(class_name, *args, **kwargs):
    (module_name, class_name) = class_name.rsplit('.', 1)
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    result = class_meta(*args, **kwargs)

    return result

def build_beautifulsop(html):
    return bs4.BeautifulSoup(html,'html.parser')


def build_analysis_style(bs,analysis_style):

    if analysis_style.get('find'):
        find_attr = analysis_style.get('find')
        return bs.find(find_attr.get('name'),attrs=find_attr.get('attrs'))if find_attr.get('name') else bs.find(attrs=find_attr.get('attrs'))
    elif analysis_style.get('select'):
        return bs.select_one(analysis_style.get('select'))
    elif analysis_style.get('selects'):
        return bs.select(analysis_style.get('selects'))


def build_execute(bs,execute):

    if execute.get('text'):
        execute_text = execute.get('text')
        if  execute_text.get('string')== False or execute_text.get('string')== True:
            if isinstance(bs,list):
                bs_result = []
                for b in bs:
                    bs_result.append(b.string if execute_text.get('string') else b.get_text())
            else:
                bs_result =  bs.string if execute_text.get('string') else bs.get_text()
        elif execute_text.get('get_attr'):
            if isinstance(bs,list):
                bs_result = []
                for b in bs:
                    bs_result.append(b.get(execute_text.get('get_attr')))
            else:
                bs_result =  bs.get(execute_text.get('get_attr'))
        else:
            raise NameError('text,get_attr : Attribute error')
    else:
        bs_result =  bs

    if execute.get('func'):
        func = execute.get('func')
        if isinstance(func,list) and not isinstance(bs_result,list):
            for f in func:
                bs_result = create_class_instance(f,bs_result)
        elif isinstance(func,list) and isinstance(bs_result,list):
            bs_re = []
            for b in bs_result:
                res = ''
                for f in func:
                    res = create_class_instance(f,bs_result)
                bs_re.append(res)
            bs_result = bs_re

        elif not isinstance(func,list) and isinstance(bs_result,list):
            bs_re = []
            for b in bs_result:
                bs_re.append(create_class_instance(func, b))
            bs_result = bs_re
        else:
            bs_result = create_class_instance(func, bs_result)

    return bs_result



def analysis(html,analysis_config={}):
    '''
    {
        "item_name":'content',
        'analysis_style':{
            # "find":{
            #     "name":'h1',
            #     "attrs":{
            #         'class':'title'
            #     }
            # },
            'select':'a',
            # 'selects': '.title',
        },
        # "execute":{
        #     "text":{
        #         # 'string':True,
        #         'get_attr':'href'
        #     },
        #     "func":'test.aa'
        # },
        # "end_execute_func":'test.aaa',

    }
    :param html:
    :param analysis_config:
    :return:
    '''

    if not isinstance(html,bs4.Tag):
        html = build_beautifulsop(html)

    if not isinstance(analysis_config,list):
        analysis_config = [analysis_config]

    data = {}
    for config in analysis_config:
        item_name = config.get('item_name')
        analysis_style = config.get('analysis_style')
        execute = config.get('execute')
        end_execute_func = config.get('end_execute_func')
        if not item_name:
            raise NameError('item_name : The name of the project must have ')
        if analysis_style:
            bs_results =  build_analysis_style(html,analysis_style)
        else:
            bs_results = html
        if execute:
            bs_results = build_execute(bs_results,execute)
        if end_execute_func:
            bs_results = create_class_instance(end_execute_func, bs_results)
        data[item_name] = bs_results
    return data




if __name__ == '__main__':
    attr = {
        "item_name":'content',
        'analysis_style':{
            # "find":{
            #     "name":'h1',
            #     "attrs":{
            #         'class':'title'
            #     }
            # },
            'select':'a',
            # 'selects': '.title',
        },
        # "execute":{
        #     "text":{
        #         # 'string':True,
        #         'get_attr':'href'
        #     },
        #     "func":'test.aa'
        # },
        # "end_execute_func":'test.aaa',

    }
