from django import template
register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
    #使い方:{{ 辞書名|get_item:変数（key） }}

@register.filter
def get_all(dictionary, key):
    return dictionary[key].items()
    #使い方:{{ for k,v in 辞書名|get_all:変数（key） }}