const user_email = "{{ current_user.email }}";
{% if current_user.shop %}
    const shop_id = "{{ current_user.shop.id }}";
{% endif %}