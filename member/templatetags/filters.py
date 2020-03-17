from django import template

register = template.Library()

@register.filter
def convert_status(value):
    status = ['결제완료', '배송중', '배송완료', '주문취소']
    return status[value]