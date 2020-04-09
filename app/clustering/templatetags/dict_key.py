from django import template
register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
    #使い方:{{ 辞書名|get_item:変数 }}