SEARCH_SQL = """
select id, title, price, currency, image_url, source_url
from products
where is_active = true
order by updated_at desc
limit :limit offset :offset
"""
